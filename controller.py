#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import random
from google.appengine.ext import ndb
import users
import data
import Cookie
import datetime

def getUsers(keys_only=False):
	return data.getUsers(keys_only)
pass



def getUsersKeys():

	l = []
	for i in data.getUsers():
		l.append({'key':i.key})
	return l

	pass

def getUser(userId):
	m_user =  data.getUser(userId)
	return m_user

def updateUser(idLink, newUser):
	return data.updateUser(idLink, newUser)

def deleteUser(userId):
	"""удаление информации о пользователе"""
	u  = data.getUser(userId)
	u.delete()

	pass

def deleteRound(byKey):

	u = data.getRoundByKey(byKey)
	u.delete()
	pass

def getCommandByID(idCommand):

	command = None
	commands = users.Commands.get_by_id(long (idCommand) )

	if (not commands==None):
		command =commands

	return command

	pass


def addUser(newUser):
	return data.addUser(newUser)
	pass

def addMatch(newMatch):
	return data.addMatch(newMatch)
	pass

def getRates():

	l = []

	users = getUsers()

	i = 1
	for u in users:

		l.append({'i':i, 'user':u, 'rate':(100 - i)})

		i =i+1 

		pass
	return l


def completeMatch(keyTour, keyMatch, left_value, right_value):

	tour = data.getRoundByKey(keyTour)

	match = data.getMatchByKey(keyMatch)

	match.left_value = int(left_value)
	match.right_value = int(right_value)
	match.result = left_value + ' : ' + right_value



	match.put()

	query = users.UserRates.get_list(key_matches=[match.key])

	l_rates = []
	for user_rate in query:

		rate = 0
		#try:

		if (user_rate.firstCommand == None or  user_rate.secondCommand == None):
			rate = 0
		elif (int(left_value) == user_rate.firstCommand and 
		int(right_value) == user_rate.secondCommand ) :

			rate = 3
		elif ((int(left_value)-int(right_value))==(user_rate.firstCommand -  user_rate.secondCommand )):
			rate = 2 # угадали победителя, разницу и ничью
		elif ((int(left_value)>int(right_value)) and (user_rate.firstCommand > user_rate.secondCommand )):
			rate = 1 # угадали победителя
		elif ((int(left_value)<int(right_value)) and (user_rate.firstCommand < user_rate.secondCommand )):
			rate = 1 # угадали победителя
		else :
			rate = 0 # ничего не угадали


		rate = rate * tour.rate

		user_rate.result = unicode(rate)
		l_rates.append(user_rate)


#		except Exception, e:
#			pass
#


		l_rates.append(user_rate)
	ndb.put_multi(l_rates)





	pass


def getMatches(key_round):


	l = []

	t = datetime.datetime.today()

	commands_map = getListCommands()


	for match in data.getMatches(key_round):

		firstCommand =commands_map[match.firstCommand.id()]
		secondCommand = commands_map[match.secondCommand.id()]

		l.append({
		'left'		: firstCommand['title'],
		'left_img'	: firstCommand['img'],

		'right'		: secondCommand['title'],
		'right_img'	: secondCommand['img'],

		'time'		: match.match_time().strftime("%d.%m %H:%M"), # %y
		'result'	: ' ' if match.result == None else match.result,
		'is_result'	: False if match.left_value == None or match.right_value ==None else True,
		'isEnd'		: (t > match.match_time())
		})
		pass

	return l

def getMatchesByGroupForUser(user, round_key):


	for match in users.Matches.get_list(round_key):
		l.append({
		'left'			:match.firstCommand.name,
		'right'			:match.secondCommand.name,
		'left_img'		:match.firstCommand.bg_picture,
		'right_img'		:match.secondCommand.bg_picture,
		'group'			:match.group,
		'id'			:match.key.id()

		})
		pass

	return l

	pass


def get_current_tour():

	tour = users.Rounds.get_current_tour()

	return tour

def getMatchesByGroup(u, round_key):

	l = []

	matches = users.Matches.get_list(round_key)

	key_matches = []

	for match in matches:
		key_matches.append(match.key)

	userRates = getUserRatesForMatches(u, key_matches)

	commands_map = getListCommands()

	t = datetime.datetime.today()

	for match in matches:

		firstCommand =commands_map[match.firstCommand.id()]
		secondCommand = commands_map[match.secondCommand.id()]

		key_id = match.key.id()

		l.append({
		'left'			: firstCommand.get('title'),
		'right'			: secondCommand.get('title'),
		'left_img'		: firstCommand.get('img'),
		'right_img'		: secondCommand.get('img'),
		'disabled'		: t>match.control_time(),
		'group'			: match.group,
		'id'			: key_id,
		'left_value'	: userRates[key_id]['left'] if ( key_id in userRates and not userRates[key_id]['left']==None)  else "",
		'right_value'	: userRates[key_id]['right'] if ( key_id in userRates and not userRates[key_id]['right']==None)  else ""
		})

		pass

	return l

def getMatchesByTour(tour_key):


	l = []
	if tour_key =="":
		return l 

	commands =users.Commands.get_dict()

	for match in data.getMatches(data.getRoundByKey(tour_key).key, "ORDER by group, matchTime"):
		left 	= commands[match.firstCommand.id()]
		right 	= commands[match.secondCommand.id()]
		l.append({
		'key'		:str(match.key.id()),
		
		'left'		: left.name,
		'left_img'	: left.bg_picture,
		
		'right'		: right.name,
		'right_img'	: right.bg_picture,
		'time'		: match.match_time().strftime("%d.%m %H:%M"), # %y
		'left_value': "" if match.left_value == None else match.left_value,
		'right_value':	"" if match.right_value== None else match.right_value,
		'group'		: match.group
		})
		pass

	return l


def checkAndGetUser(webapp, redirect_if_error = True):
	"""Проверяем был ли передан ID пользователя, если был, тогда устанавливаем это значение в кукисах.
	Если не был, тогда возвращаем None

	"""


	# id
	auth = None

	auth = webapp.request.get('auth')

	if (not auth == ""):

		t = datetime.datetime.today()
		t = t + datetime.timedelta(days=30)
		# устанавливаем куку и срок окончания, по умолчанию берем 30 дней
 		webapp.response.headers['Set-Cookie'] = "auth=" + str(auth) + "; expires=" + t.strftime("%a, %d-%b-%y 12:00:00 GMT")
	elif 'auth' in  webapp.request.cookies:
		auth = webapp.request.cookies['auth']
	else:
		auth = None



	u = data.getUserByAuth(auth)

	if u == None and redirect_if_error:
		webapp.redirect("/auth_error" )


	return u


	pass


def updateUserRates(user_rates):
	ndb.delete_multi([x.key for x in user_rates if not x.key==None])
	ndb.put_multi([x for x in user_rates if not (x.firstCommand==None and x.secondCommand==None) ]) 

	pass

def getAllMatches():

	l = []
	commands = getListCommands()

#	for tour in data.getRounds():

	for match in data.getMatches():

		leftCommand = commands.get(users.Matches.firstCommand.get_value_for_datastore(match).id())
		rightCommand = commands.get(users.Matches.secondCommand.get_value_for_datastore(match).id())

		l.append({'left':leftCommand.get('title'),
		'right':rightCommand.get('title'),
		'left_img':leftCommand.get('img'),
		'right_img':rightCommand.get('img')
		})

	pass

	return l

def getMatchRates(r):


	matches = data.getMatches(r,keys_only=True)
	key_matches = []
	for m in matches:
		key_matches.append(m)



	# здесь необходимо представление пользователь \ результаты матчей

	# Делаем быстрое и тупое решение


	allusers = getUsers()
	l = []

#	results= 	ndb.GqlQuery("SELECT * FROM UserRates WHERE user=:1 and match in :2", u.key(), key_matches).fetch(1000)
	match_results = getUserRatesForAllUsers(key_matches)

	for u in allusers:
		user_key = long(u.key.id())
		for m in key_matches:
			key_id = long(m.id())

			if user_key in match_results and key_id in match_results[user_key]:
				result = match_results[user_key][key_id]

				l.append({'user':u,
					'is_rate': True, 
					'left': result['left'], 
					'right':result['right'], 
					'result':result['result'], 
					'is_result':result['is_result']
					})
			else:
				l.append({'user':u,
					'is_rate': False})

		


	return l
pass

def getRoundByKey(key):
	if key =="":
		return {}
	else:
		return users.Rounds.get_by_id(long(key))


pass
 
def editRate(key_value, new_value):

	"""Устанавливаем новый рейтинг для туров"""
	if key_value =="":
		return
	else:

		# устанавливаем значение по умолчанию
		if new_value == "":
			new_value = 1.0

		# Обновляем результат матча
		match = data.getRoundByKey(key_value)
		match.rate = float(new_value)
		match.put()

	pass


def getMatch(id_match):
	return data.getMatch(id_match)

	pass
def getMatchView(key_value):

	match = data.getMatch(key_value)

	m = {}

	m['key'] = key_value
	m['group'] = match.group
	m['date_day'] = match.match_time().strftime("%d.%m.%Y")
	m['date_time'] = match.match_time().strftime("%H:%M")
	m['firstCommand'] = match.firstCommand.id()
	m['secondCommand'] = match.secondCommand.id()

	return m

def getUserRates(u, m):
	"""Получаем значения ставок пользователя, те которые делал он"""

	return data.getUserRates(u, m)
	pass

def getUserRatesForMatches(u, key_matches):
	results= users.UserRates.get_list (u.key, key_matches)

	#ndb.GqlQuery("SELECT * FROM UserRates WHERE user=:1 and match in :2", u.key, key_matches).fetch(60)

	m ={}
	for en in results: #users.UserRates.gql("WHERE user=:1 and match in :2", u.key(), key_matches):
		m[en.match.id()] = {
		'left':en.firstCommand if not en.firstCommand == None else 0, 
		'right':en.secondCommand if not en.secondCommand ==None else 0 }
	
	return m 

def getUserRatesForAllUsers(key_matches=None):

	

	m ={}

	user_rates = users.UserRates.get_list(key_matches=None)
	for entity in user_rates:
		match_res = {
		'left'			: entity.firstCommand	if not entity.firstCommand == None 	else "", 
		'result'		: entity.result			if not entity.result == None 		else "", 
		'is_result'		: True					if not entity.result == None 		else False, 
		'right'			: entity.secondCommand	if not entity.secondCommand ==None 	else "" 
		}

		user_key = entity.user.id()
		match_key = entity.match.id()

		if user_key in m:

			m[user_key][match_key] = match_res

		else:
			m[user_key] = {match_key:match_res}
	
	return m



def getUserRatesForUsers(m, key_users):
	m ={}
	for en in users.UserRates.gql("WHERE user=:1 and match = :2", key_users, m):
		m[en.user.key.id()] = {
		'left':en.firstCommand, 
		'right':en.secondCommand}
	
	return m


def deleteMatcIh(key_value):

	if (key_value == "" or key_value==None):
		return


	m = data.getMatchByKey(key_value)

	if (m == None):
		return
	m.delete()
	pass


def getAllMatchRates():

	matches = data.getMatches(keys_only=True)
	key_matches = []
	for m in matches:
		key_matches.append(m)



	# здесь необходимо представление пользователь \ результаты матчей

	# Делаем быстрое и тупое решение


	allusers = getUsers()
	l = []

#	results= 	ndb.GqlQuery("SELECT * FROM UserRates WHERE user=:1 and match in :2", u.key(), key_matches).fetch(1000)
	match_results = getUserRatesForAllUsers()

	for u in allusers:
		user_key = long(u.key.id())
		for m in key_matches:
			key_id = long(m.id())

			if user_key in match_results and key_id in match_results[user_key]:
				result = match_results[user_key][key_id]
				if (result['left'] == None and result['right'] == None):
					l.append({'user':u, 'rate':"-1--"})
				else:
					l.append({'user':u, 'rate':"%s : %s" % (
						"0" if result['left'] == None else result['left'], 
						"0" if result['right'] == None else result['right']
						)})
			else:
				l.append({'user':u, 'rate':"-2--"})
		


	return l	

def getTournaments():
	"""Возвращаемое значение title, games {left,right,left_img,right_img,values}"""

	tours =[]

	for tour in data.getRounds():
		games = []


		for match in data.getMatches(tour):
			games.append({'left':match.firstCommand.name,
			'right':match.secondCommand.name,
			'left_img':match.firstCommand.bg_picture,
			'right_img':match.secondCommand.bg_picture,
			'values':"%d : %d" % (random.randint(1,9),random.randint(1,9))
			})

			pass

		tours.append({'title':tour.title, "games":games})
		pass

	return tours

	pass


def getCommands():
	"""Возвращает структуру title, img"""

	l = []
	commands = users.Commands.get_list()


	for command in commands:
		l.append({"title":command.name, "img":command.bg_picture,"key":command.key.id()})
	return l


def getListCommands():
	"""Возвращает структуру title, img"""

#	commands =  users.Commands.all()
#	commands = ndb.GqlQuery("SELECT * FROM Commands").fetch(20)
	commands = users.Commands.query().order(users.Commands.name).fetch(40)

	m = {}

	for command in commands:
		m[command.key.id()] = {"title":unicode(command.name), "img":str(command.bg_picture)}

	return m

def getRounds():
	"""Возвращаем список туров"""

	return data.getRounds()

def getRound(by_id):
	"""Возвращаем тур"""

	return data.getRound(by_id)





