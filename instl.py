#!/usr/bin/env python
# -*- coding: utf-8 -*-

import users
import utils
import random
#from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.ext import ndb
import datetime
import string

def installMatches(interval = 0):

	# 1. загружаем туры

	ndb.delete_multi(users.UserRates.query().fetch(2000, keys_only=True))
	ndb.delete_multi(users.UserResults.query().fetch(2000, keys_only=True))
	ndb.delete_multi(users.Matches.query().fetch(2000, keys_only=True))

	fillMatches(interval)

	pass

def clearUser():
	#users.Users.delete_multi()
	ndb.delete_multi(users.Users.query().fetch(2000, keys_only=True))
	ndb.delete_multi(users.UserRates.query().fetch(2000, keys_only=True))
	ndb.delete_multi(users.UserResults.query().fetch(2000, keys_only=True))


def installRounds():

	ndb.delete_multi(users.Rounds.query().fetch(2000, keys_only=True))

	l = []

	l.append({'title':u"Тур 1", 'rate':1.0})
	l.append({'title':u"Тур 2", 'rate':1.0})
	l.append({'title':u"Тур 3", 'rate':1.0})
	l.append({'title':u"1/8 финала", 'rate':1.0})
	l.append({'title':u"1/4 финала", 'rate':1.0})
	l.append({'title':u"Полуфинал", 'rate':1.5})
	l.append({'title':u"Финал", 'rate':2.0})


	number_order = 1

	entities = []
	for r in l :
		entity = users.Rounds(title = r['title'])
		entity.rate = float(r['rate'])
		entity.order = number_order

		entities.append(entity)

		number_order = number_order +1


	ndb.put_multi(entities)
	pass




def fillMatches(interval):

	l = []

	l.append({'left':u"Франция",  			'right':u"Румыния",     		'dates' : "10.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа А", 'tour' : u"Тур 1"})
	l.append({'left':u"Албания",  			'right':u"Швейцария",     		'dates' : "11.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа А", 'tour' : u"Тур 1"})
	l.append({'left':u"Уэльс",  			'right':u"Словакия",     		'dates' : "11.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 1"})
	l.append({'left':u"Англия",  			'right':u"Россия",     			'dates' : "11.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 1"})
	l.append({'left':u"Турция",  			'right':u"Хорватия",     		'dates' : "12.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 1"})
	l.append({'left':u"Польша",  			'right':u"Северная Ирландия",   'dates' : "12.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа С", 'tour' : u"Тур 1"})
	l.append({'left':u"Германия",  			'right':u"Украина",     		'dates' : "12.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа С", 'tour' : u"Тур 1"})
	l.append({'left':u"Испания",  			'right':u"Чехия",     			'dates' : "13.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 1"})
	l.append({'left':u"Ирландия",  			'right':u"Швеция",     			'dates' : "13.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 1"})
	l.append({'left':u"Бельгия",  			'right':u"Италия",     			'dates' : "13.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 1"})
	l.append({'left':u"Австрия",  			'right':u"Венгрия",     		'dates' : "14.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 1"})
	l.append({'left':u"Португалия",  		'right':u"Исландия",     		'dates' : "14.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 1"})
	l.append({'left':u"Россия",  			'right':u"Словакия",     		'dates' : "15.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 2"})
	l.append({'left':u"Румыния",  			'right':u"Швейцария",     		'dates' : "15.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа А", 'tour' : u"Тур 2"})
	l.append({'left':u"Франция",  			'right':u"Албания",     		'dates' : "15.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа А", 'tour' : u"Тур 2"})
	l.append({'left':u"Англия",  			'right':u"Уэльс",     			'dates' : "16.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 2"})
	l.append({'left':u"Украина",  			'right':u"Северная Ирландия",   'dates' : "16.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа С", 'tour' : u"Тур 2"})
	l.append({'left':u"Германия",  			'right':u"Польша",     			'dates' : "16.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа С", 'tour' : u"Тур 2"})
	l.append({'left':u"Италия",  			'right':u"Швеция",     			'dates' : "17.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 2"})
	l.append({'left':u"Чехия",  			'right':u"Хорватия",     		'dates' : "17.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 2"})
	l.append({'left':u"Испания",  			'right':u"Турция",     			'dates' : "17.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 2"})
	l.append({'left':u"Бельгия",  			'right':u"Ирландия",     		'dates' : "18.06.2016T15:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 2"})
	l.append({'left':u"Исландия",  			'right':u"Венгрия",     		'dates' : "18.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 2"})
	l.append({'left':u"Португалия",  		'right':u"Австрия",     		'dates' : "18.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 2"})
	l.append({'left':u"Швейцария",  		'right':u"Франция",     		'dates' : "19.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа А", 'tour' : u"Тур 3"})
	l.append({'left':u"Румыния",  			'right':u"Албания",     		'dates' : "19.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа А", 'tour' : u"Тур 3"})
	l.append({'left':u"Словакия",  			'right':u"Англия",     			'dates' : "20.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 3"})
	l.append({'left':u"Россия",  			'right':u"Уэльс",     			'dates' : "20.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 3"})
	l.append({'left':u"Северная Ирландия",  'right':u"Германия",     		'dates' : "21.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа С", 'tour' : u"Тур 3"})
	l.append({'left':u"Украина",  			'right':u"Польша",     			'dates' : "21.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа С", 'tour' : u"Тур 3"})
	l.append({'left':u"Хорватия",  			'right':u"Испания",     		'dates' : "21.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 3"})
	l.append({'left':u"Чехия",  			'right':u"Турция",     			'dates' : "21.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 3"})
	l.append({'left':u"Исландия",  			'right':u"Австрия",     		'dates' : "22.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 3"})
	l.append({'left':u"Венгрия",  			'right':u"Португалия",     		'dates' : "22.06.2016T18:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 3"})
	l.append({'left':u"Швеция",  			'right':u"Бельгия",     		'dates' : "22.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 3"})
	l.append({'left':u"Италия",  			'right':u"Ирландия",     		'dates' : "22.06.2016T21:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 3"})


	time = datetime.datetime.today() + datetime.timedelta(hours=2)

	commands = users.Commands.get_dict('name')
	tours  = users.Rounds.get_dict('title')
	print ("%s" % users.Rounds.get_list() )

	l_matches = []
	for m in l :

		if interval > 0:
			time = time + datetime.timedelta(minutes=interval)
		else:
			fmt = "%d.%m.%YT%H:%M"
			time = datetime.datetime.utcnow().strptime (m['dates'], fmt)
			#split_dt = m['dates'].split(" ")
			#time = getDateTime(split_dt[0], split_dt[1], split_dt[2]) - datetime.timedelta(hours=4) # вводим время с учетом часового пояса

		match = putMatch(left=commands[m['left']], right=commands[m['right']], dates = time, group=m['group'], tour =tours[m['tour']])
		l_matches.append(match)
		
		# l_matches.append(putMatch(left=commands[m['left']], right=commands[m['right']], dates = time, group=m['group'], tour =tours[m['tour']]))

	ndb.put_multi(l_matches)
	pass

def putMatch(left,right,dates,group, tour):
	print ("COMMAND %s" % left)
	print ("COMMAND %s" % right)
	print ("tour %s" % tour)

	entity = users.Matches()

	entity.firstCommand = left
	entity.secondCommand = right
	entity.group = group
	entity.tour = tour
	entity.endTime = str(dates)
	entity.matchTime = dates
	return entity

	pass


# def getCommand(title):
# 
# 	c = GqlQuery("SELECT __key__ FROM Commands WHERE name=:1", title)
# 	return c[0]
# 	pass
# 
# def getRound(title):
# 
# 	c = users.Rounds.gql("WHERE title = :1", title)
# 	return c[0]
# 	pass

def installCommands():

#	installRounds()
	ndb.delete_multi( users.Commands.query().fetch(100, keys_only=True))

	#print "generate commands"
	comm = getCommands()
	for c in comm:

		# загружаем список комманд

		entity = users.Commands(name=c)
		entity.bg_picture = comm[c]
		entity.small_picture = comm[c]

		entity.put()
		pass


	pass


def addUser(firstName, secondName, lastName, mail=""):

	if secondName == u"":
		title = "%s %s." % (lastName ,  firstName[0])
	else:
		title = "%s %s.%s." % (lastName ,  firstName[0] , secondName[0])

	entity = users.Users()
	entity.title = title
	entity.altTitle = firstName + " " +  secondName
	entity.lastName = lastName
	entity.firstName = firstName
	entity.secondName = secondName
	entity.mail = mail
	entity.idLink = utils.generateID(10)

	return entity


	pass




def fillUsers():

	clearUser()

	l_users = []

	l_users.append(addUser(u"Ольга", u"Вячеславовна", u"Карпушина"))

	ndb.put_multi(l_users)


	r_matches = users.Matches.all(keys_only=True)
	r_users = users.Users.all(keys_only=True)

	l_entities = []

	for u in r_users:
		for m in r_matches:

			rate = users.UserRates()
			rate.user = u
			rate.match = m
			rate.firstCommand = int(random.random()*5)
			rate.secondCommand = int(random.random()*5)
			l_entities.append(rate)

			res = users.UserResults()
			res.user = u
			res.match = m
			res.value = int(random.random()*5)
			l_entities.append(res)

	ndb.put_multi(l_entities)

#



	pass


def delete_double():


	db_user = users.UserRates.query().fetch(1000)

	l = []
	for entity in db_user:
		l.append({'user':entity.user.id(),'match':entity.match.id(),'id':entity.key.id()})

	# сортируем результат игры и выводим итоговую таблицу
	sorted_rating_list = sorted(l, key=lambda k: (k['user'], k['match'], -k['id']) )
	print "<pre>"
	print sorted_rating_list

	d = []
	prev = {'user':0L, 'match':0L}
	for entity in sorted_rating_list :

		if (prev['user'] == entity['user'] and prev['match'] == entity['match']):
			d.append(users.UserRates.get_by_id(entity['id']))

		prev['user'] = entity['user']
		prev['match'] = entity['match']

	print d

	db.delete(d)


	print "</pre>"




#	print sorted_rating_list









def fillBrunswick():

	clearUser()

	l_users = []
	ndb.put_multi(l_users)

	return
#	r_matches = users.Matches.all(keys_only=True)
#	r_users = users.Users.all(keys_only=True)
#
#	l_entities = []
#
#	for u in r_users:
#		for m in r_matches:
#
#			rate = users.UserRates()
#			rate.user = u
#			rate.match = m
#			rate.firstCommand = int(random.random()*5)
#			rate.secondCommand = int(random.random()*5)
#			l_entities.append(rate)
#
#			res = users.UserResults()
#			res.user = u
#			res.match = m
#			res.value = int(random.random()*5)
#			l_entities.append(res)
#
#	ndb.put_multi(l_entities)


pass



def getCommands():

	t = {

	u"":"",

	u"Албания":"flag-al",
	u"Австрия":"flag-at",
	u"Бельгия":"flag-be",
	u"Швейцария":"flag-ch",

	u"Чехия":"flag-cz",
	u"Германия":"flag-de",
	u"Англия":"flag-england",
	u"Испания":"flag-es",

	u"Франция":"flag-fr",

	u"Венгрия":"flag-hu",
	u"Ирландия":"flag-ie",

	u"Исландия":"flag-is",
	u"Италия":"flag-it",
	u"Польша":"flag-pl",
	u"Португалия":"flag-pt",

	u"Румыния":"flag-ro",
	u"Россия":"flag-ru",
	u"Швеция":"flag-se",
	u"Хорватия":"flag-sk",

	u"Турция":"flag-tr",
	u"Украина":"flag-ua",
	u"Уэльс":"flag-wales",
	u"Северная Ирландия": "flag-england"


	}


	return t


