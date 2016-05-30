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

	l.append({'left':u"Бразилия", 				'right':u"Хорватия", 				'dates' : "12.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа A", 'tour' : u"Тур 1"})
	l.append({'left':u"Мексика", 				'right':u"Камерун", 				'dates' : "13.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа A", 'tour' : u"Тур 1"})
	l.append({'left':u"Камерун", 				'right':u"Хорватия", 				'dates' : "18.06.2014T18:00", 'UTC':"-0300", 'group':u"Группа A", 'tour' : u"Тур 2"})
	l.append({'left':u"Бразилия", 				'right':u"Мексика", 				'dates' : "17.06.2014T16:00", 'UTC':"-0400", 'group':u"Группа A", 'tour' : u"Тур 2"})
	l.append({'left':u"Камерун", 				'right':u"Бразилия", 				'dates' : "23.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа A", 'tour' : u"Тур 3"})
	l.append({'left':u"Хорватия", 				'right':u"Мексика", 				'dates' : "23.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа A", 'tour' : u"Тур 3"})
	l.append({'left':u"Испания", 				'right':u"Нидерланды", 				'dates' : "13.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 1"})
	l.append({'left':u"Чили", 					'right':u"Австралия", 				'dates' : "13.06.2014T18:00", 'UTC':"-0400", 'group':u"Группа B", 'tour' : u"Тур 1"})
	l.append({'left':u"Испания", 				'right':u"Чили", 					'dates' : "18.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 2"})
	l.append({'left':u"Австралия", 				'right':u"Нидерланды", 				'dates' : "18.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 2"})
	l.append({'left':u"Австралия", 				'right':u"Испания", 				'dates' : "23.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 3"})
	l.append({'left':u"Нидерланды", 			'right':u"Чили", 					'dates' : "23.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа B", 'tour' : u"Тур 3"})
	l.append({'left':u"Колумбия", 				'right':u"Греция", 					'dates' : "14.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа C", 'tour' : u"Тур 1"})
	l.append({'left':u"Кот-д’Ивуар", 			'right':u"Япония", 					'dates' : "14.06.2014T22:00", 'UTC':"-0300", 'group':u"Группа C", 'tour' : u"Тур 1"})
	l.append({'left':u"Колумбия", 				'right':u"Кот-д’Ивуар", 			'dates' : "19.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа C", 'tour' : u"Тур 2"})
	l.append({'left':u"Япония", 				'right':u"Греция", 					'dates' : "19.06.2014T19:00", 'UTC':"-0300", 'group':u"Группа C", 'tour' : u"Тур 2"})
	l.append({'left':u"Япония", 				'right':u"Колумбия", 				'dates' : "24.06.2014T16:00", 'UTC':"-0400", 'group':u"Группа C", 'tour' : u"Тур 3"})
	l.append({'left':u"Греция", 				'right':u"Кот-д’Ивуар", 			'dates' : "24.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа C", 'tour' : u"Тур 3"})
	l.append({'left':u"Уругвай", 				'right':u"Коста-Рика", 				'dates' : "14.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 1"})
	l.append({'left':u"Англия", 				'right':u"Италия", 					'dates' : "14.06.2014T18:00", 'UTC':"-0400", 'group':u"Группа D", 'tour' : u"Тур 1"})
	l.append({'left':u"Уругвай", 				'right':u"Англия", 					'dates' : "19.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 2"})
	l.append({'left':u"Италия", 				'right':u"Коста-Рика", 				'dates' : "20.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 2"})
	l.append({'left':u"Италия", 				'right':u"Уругвай", 				'dates' : "24.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 3"})
	l.append({'left':u"Коста-Рика", 			'right':u"Англия", 					'dates' : "24.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа D", 'tour' : u"Тур 3"})
	l.append({'left':u"Швейцария", 				'right':u"Эквадор", 				'dates' : "15.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 1"})
	l.append({'left':u"Франция", 				'right':u"Гондурас", 				'dates' : "15.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 1"})
	l.append({'left':u"Швейцария", 				'right':u"Франция", 				'dates' : "20.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 2"})
	l.append({'left':u"Гондурас", 				'right':u"Эквадор", 				'dates' : "20.06.2014T19:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 2"})
	l.append({'left':u"Гондурас", 				'right':u"Швейцария", 				'dates' : "25.06.2014T16:00", 'UTC':"-0400", 'group':u"Группа E", 'tour' : u"Тур 3"})
	l.append({'left':u"Эквадор", 				'right':u"Франция", 				'dates' : "25.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа E", 'tour' : u"Тур 3"})
	l.append({'left':u"Аргентина", 				'right':u"Босния и Герцеговина", 	'dates' : "15.06.2014T19:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 1"})
	l.append({'left':u"Иран", 					'right':u"Нигерия", 				'dates' : "16.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 1"})
	l.append({'left':u"Аргентина", 				'right':u"Иран", 					'dates' : "21.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 2"})
	l.append({'left':u"Нигерия", 				'right':u"Босния и Герцеговина", 	'dates' : "21.06.2014T18:00", 'UTC':"-0400", 'group':u"Группа F", 'tour' : u"Тур 2"})
	l.append({'left':u"Нигерия", 				'right':u"Аргентина", 				'dates' : "25.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 3"})
	l.append({'left':u"Босния и Герцеговина", 	'right':u"Иран", 					'dates' : "25.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа F", 'tour' : u"Тур 3"})
	l.append({'left':u"Германия", 				'right':u"Португалия", 				'dates' : "16.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа G", 'tour' : u"Тур 1"})
	l.append({'left':u"Гана", 					'right':u"США", 					'dates' : "16.06.2014T19:00", 'UTC':"-0300", 'group':u"Группа G", 'tour' : u"Тур 1"})
	l.append({'left':u"Германия", 				'right':u"Гана", 					'dates' : "21.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа G", 'tour' : u"Тур 2"})
	l.append({'left':u"США", 					'right':u"Португалия", 				'dates' : "22.06.2014T18:00", 'UTC':"-0400", 'group':u"Группа G", 'tour' : u"Тур 2"})
	l.append({'left':u"США", 					'right':u"Германия", 				'dates' : "26.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа G", 'tour' : u"Тур 3"})
	l.append({'left':u"Португалия", 			'right':u"Гана", 					'dates' : "26.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа G", 'tour' : u"Тур 3"})
	l.append({'left':u"Бельгия", 				'right':u"Алжир", 					'dates' : "17.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа H", 'tour' : u"Тур 1"})
	l.append({'left':u"Россия", 				'right':u"Корея", 					'dates' : "17.06.2014T18:00", 'UTC':"-0400", 'group':u"Группа H", 'tour' : u"Тур 1"})
	l.append({'left':u"Бельгия", 				'right':u"Россия", 					'dates' : "22.06.2014T13:00", 'UTC':"-0300", 'group':u"Группа H", 'tour' : u"Тур 2"})
	l.append({'left':u"Корея", 					'right':u"Алжир", 					'dates' : "22.06.2014T16:00", 'UTC':"-0300", 'group':u"Группа H", 'tour' : u"Тур 2"})
	l.append({'left':u"Корея", 					'right':u"Бельгия", 				'dates' : "26.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа H", 'tour' : u"Тур 3"})
	l.append({'left':u"Алжир", 					'right':u"Россия", 					'dates' : "26.06.2014T17:00", 'UTC':"-0300", 'group':u"Группа H", 'tour' : u"Тур 3"})


#	l.append({'left':u"Польша", 'right':u"Греция", 'dates' : "08.06.12 20:00", 'group':u"Группа A", 'tour' : u"Тур 1"})
#	l.append({'left':u"Россия", 'right':u"Чехия", 'dates' : "08.06.12 22:45", 'group':u"Группа A", 'tour' : u"Тур 1"})
#	l.append({'left':u"Нидерланды", 'right':u"Дания", 'dates' : "09.06.12 20:00", 'group':u"Группа B", 'tour' : u"Тур 1"})
#	l.append({'left':u"Германия", 'right':u"Португалия", 'dates' : "09.06.12 22:45", 'group':u"Группа B", 'tour' : u"Тур 1"})
#	l.append({'left':u"Испания", 'right':u"Италия", 'dates' : "10.06.12 20:00", 'group':u"Группа C", 'tour' : u"Тур 1"})
#	l.append({'left':u"Ирландия", 'right':u"Хорватия", 'dates' : "10.06.12 22:45", 'group':u"Группа C", 'tour' : u"Тур 1"})
#	l.append({'left':u"Франция", 'right':u"Англия", 'dates' : "11.06.12 20:00", 'group':u"Группа D", 'tour' : u"Тур 1"})
#	l.append({'left':u"Украина", 'right':u"Швеция", 'dates' : "11.06.12 22:45", 'group':u"Группа D", 'tour' : u"Тур 1"})
#
#
#	l.append({'left':u"Греция", 'right':u"Чехия", 'dates' : "12.06.12 20:00", 'group':u"Группа A", 'tour' : u"Тур 2"})
#	l.append({'left':u"Польша", 'right':u"Россия", 'dates' : "12.06.12 22:45", 'group':u"Группа A", 'tour' : u"Тур 2"})
#	l.append({'left':u"Дания", 'right':u"Португалия", 'dates' : "13.06.12 20:00", 'group':u"Группа B", 'tour' : u"Тур 2"})
#	l.append({'left':u"Нидерланды", 'right':u"Германия", 'dates' : "13.06.12 22:45", 'group':u"Группа B", 'tour' : u"Тур 2"})
#	l.append({'left':u"Италия", 'right':u"Хорватия", 'dates' : "14.06.12 20:00", 'group':u"Группа C", 'tour' : u"Тур 2"})
#	l.append({'left':u"Испания", 'right':u"Ирландия", 'dates' : "14.06.12 22:45", 'group':u"Группа C", 'tour' : u"Тур 2"})
#	l.append({'left':u"Швеция", 'right':u"Англия", 'dates' : "15.06.12 20:00", 'group':u"Группа D", 'tour' : u"Тур 2"})
#	l.append({'left':u"Украина", 'right':u"Франция", 'dates' : "15.06.12 22:45", 'group':u"Группа D", 'tour' : u"Тур 2"})
#
#	l.append({'left':u"Греция", 'right':u"Россия", 'dates' : "16.06.12 22:45", 'group':u"Группа A", 'tour' : u"Тур 3"})
#	l.append({'left':u"Чехия", 'right':u"Польша", 'dates' : "16.06.12 22:45", 'group':u"Группа A", 'tour' : u"Тур 3"})
#	l.append({'left':u"Португалия", 'right':u"Нидерланды", 'dates' : "17.06.12 22:45", 'group':u"Группа B", 'tour' : u"Тур 3"})
#	l.append({'left':u"Дания", 'right':u"Германия", 'dates' : "17.06.12 22:45", 'group':u"Группа B", 'tour' : u"Тур 3"})
#	l.append({'left':u"Хорватия", 'right':u"Испания", 'dates' : "18.06.12 22:45", 'group':u"Группа C", 'tour' : u"Тур 3"})
#	l.append({'left':u"Италия", 'right':u"Ирландия", 'dates' : "18.06.12 22:45", 'group':u"Группа C", 'tour' : u"Тур 3"})
#	l.append({'left':u"Швеция", 'right':u"Франция", 'dates' : "19.06.12 22:45", 'group':u"Группа D", 'tour' : u"Тур 3"})
#	l.append({'left':u"Англия", 'right':u"Украина", 'dates' : "19.06.12 22:45", 'group':u"Группа D", 'tour' : u"Тур 3"})

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

	l_users.append(addUser(u"Алексей",u"Игоревич",u"Цыплаков","atsyplakov@uniwagon.com"))
	l_users.append(addUser(u"Михаил",u"Иванович",u"Плохих","mplokhikh@uniwagon.com"))
	l_users.append(addUser(u"Екатерина",u"Александровна",u"Качанова","ekachanova@uniwagon.com"))
	l_users.append(addUser(u"Фотий",u"Пифагорович",u"Янаков","fyanakov@uniwagon.com"))
	l_users.append(addUser(u"Анна",u"Александровна",u"Петрова","apetrova@uniwagon.com"))
	l_users.append(addUser(u"Наталья",u"Сергеевна",u"Шабан","nshaban@uniwagon.com"))
	l_users.append(addUser(u"Наталия",u"Александровна",u"Тюмина","ntyumina@uniwagon.com"))
	l_users.append(addUser(u"Ксения",u"Вадимовна",u"Ульянова","kulyanova@uniwagon.com"))
	l_users.append(addUser(u"Антон",u"Викторович",u"Сайкин","asaykin@uniwagon.com"))
	l_users.append(addUser(u"Ирина",u"Валерьевна",u"Цыплакова","itsyplakova@uniwagon.com"))
	l_users.append(addUser(u"Дмитрий",u"Вячеславович",u"Бородин","dborodin@uniwagon.com"))
	l_users.append(addUser(u"Артем",u"Владимирович",u"Новокшанов","anovokshanov@uniwagon.com"))
	l_users.append(addUser(u"Александр",u"Робертович",u"Годеев","agodeev@uniwagon.com"))
	l_users.append(addUser(u"Любовь",u"Олеговна",u"Дорошева","ldorosheva@uniwagon.com"))
	l_users.append(addUser(u"Дмитрий",u"Игоревич",u"Жарков","dzharkov@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Евгеньевна",u"Ильинская","oilyinskaya@uniwagon.com"))
	l_users.append(addUser(u"Анна",u"Александровна",u"Могутова","amogutova@uniwagon.com"))
	l_users.append(addUser(u"Александра",u"Геннадьевна",u"Хрящева","akhryashcheva@uniwagon.com"))
	l_users.append(addUser(u"Иван",u"Михайлович",u"Коробейников","ikorobeynikov@uniwagon.com"))
	l_users.append(addUser(u"Альбина",u"Ринатовна",u"Хисматуллина","akhismatullina@uniwagon.com"))
	l_users.append(addUser(u"Ирина",u"Валерьевна",u"Архангельская","iarkhangelskaya@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Валерьевна",u"Ковалева","okovaleva@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Александровна",u"Хромочкина","oshershenkova@uniwagon.com"))
	l_users.append(addUser(u"Ирина",u"Александровна",u"Шульгина","ishulgina@uniwagon.com"))
	l_users.append(addUser(u"Елена",u"Александровна",u"Хвостова","ekhvostova@uniwagon.com"))
	l_users.append(addUser(u"Наталья",u"Юрьевна",u"Китаева","nkitaeva@uniwagon.com"))
	l_users.append(addUser(u"Юлия",u"Геннадьевна",u"Черенкова","ycherenkova@uniwagon.com"))
	l_users.append(addUser(u"Наталья",u"Николаевна",u"Уварова","nuvarova@uniwagon.com"))
	l_users.append(addUser(u"Лилит",u"Арменовна",u"Аветисян","lavetisyan@uniwagon.com"))
	l_users.append(addUser(u"Екатерина",u"Викторовна",u"Кондратенко","ekondratenko@uniwagon.com"))
	l_users.append(addUser(u"Валентина",u"Михайловна",u"Заварзина","vzavarzina@uniwagon.com"))
	l_users.append(addUser(u"Наталия",u"Сергеевна",u"Пискарева","npiskareva@uniwagon.com"))
	l_users.append(addUser(u"Дмитрий",u"Александрович",u"Бовыкин","dbovykin@uniwagon.com"))
	l_users.append(addUser(u"Олег",u"Михайлович",u"Дымич","odymich@uniwagon.com"))
	l_users.append(addUser(u"Владислав",u"Викторович",u"Масенков","vmasenkov@uniwagon.com"))
	l_users.append(addUser(u"Александр",u"Вацлавович",u"Зданевич","azdanevich@uniwagon.com"))
	l_users.append(addUser(u"Илья",u"Викторович",u"Зенкин","izenkin@uniwagon.com"))
	l_users.append(addUser(u"Евгений",u"Евгеньевич",u"Волков","evolkov@uniwagon.com"))
	l_users.append(addUser(u"Александра",u"Александровна",u"Гришина","agrishina@uniwagon.com"))
	l_users.append(addUser(u"Александр",u"Владимирович",u"Кинжалов","akinzhalov@uniwagon.com"))
	l_users.append(addUser(u"Руслан",u"Сергеевич",u"Желубовский","rzhelubovskiy@uniwagon.com"))
	l_users.append(addUser(u"Андрей",u"Владимирович",u"Жуков","azhukov@uniwagon.com"))
	l_users.append(addUser(u"Денис",u"Юрьевич",u"Московченко","dmoskovchenko@uniwagon.com"))
	l_users.append(addUser(u"Павел",u"Михайлович",u"Крижановский","pkrizhanovskiy@uniwagon.com"))
	l_users.append(addUser(u"Константин",u"Георгиевич",u"Дубовик","kdubovik@uniwagon.com"))
	l_users.append(addUser(u"Василий",u"Дмитриевич",u"Сомов","vsomov@uniwagon.com"))
	l_users.append(addUser(u"Лилия",u"Владимировна",u"Лаврова","llavrova@uniwagon.com"))
	l_users.append(addUser(u"Елена",u"Александровна",u"Козлова","ekozlova@uniwagon.com"))
	l_users.append(addUser(u"Светлана",u"Дмитриевна",u"Бобина","sbobina@uniwagon.com"))
	l_users.append(addUser(u"Анастасия",u"Александровна",u"Комкова","akomkova@uniwagon.com"))
	l_users.append(addUser(u"Нина",u"Павловна",u"Борисенко","nborisenko@uniwagon.com"))
	l_users.append(addUser(u"Дмитрий",u"Владимирович",u"Жиляев","dzhilyaev@uniwagon.com"))
	l_users.append(addUser(u"Лейсана",u"Растэмовна",u"Гизатуллина","lgizatullina@uniwagon.com"))
	l_users.append(addUser(u"Глеб",u"Сергеевич",u"Канин","gkanin@uniwagon.com"))
	l_users.append(addUser(u"Иван",u"Дмитриевич",u"Нырков","inyrkov@uniwagon.com"))
	l_users.append(addUser(u"Александр",u"Иванович",u"Лукьяненко","alukyanenko@uniwagon.com"))
	l_users.append(addUser(u"Илья",u"Владимирович",u"Шиян","ishiyan@uniwagon.com"))
	l_users.append(addUser(u"Дарья",u"Артемовна",u"Суздалева","dsuzdaleva@uniwagon.com"))
	l_users.append(addUser(u"Мария",u"Владимировна",u"Львова","mlvova@uniwagon.com"))
	l_users.append(addUser(u"Людмила",u"Алексеевна",u"Пахомова","lpakhomova@uniwagon.com"))
	l_users.append(addUser(u"Оксана",u"Владимировна",u"Харузина","okharuzina@uniwagon.com"))
	l_users.append(addUser(u"Анна",u"Вячеславовна",u"Кротова","akrotova@uniwagon.com"))
	l_users.append(addUser(u"Дина",u"Вениаминовна",u"Ройтман","droytman@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Валерьевна",u"Малышева","omalysheva@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Александровна",u"Гордеева","ogordeeva@uniwagon.com"))
	l_users.append(addUser(u"Анна",u"Станиславовна",u"Дзасеева","adzaseeva@uniwagon.com"))
	l_users.append(addUser(u"Мария",u"Владимировна",u"Личагина","mlichagina@uniwagon.com"))
	l_users.append(addUser(u"Руслан",u"Аманович",u"Назаров","rnazarov@uniwagon.com"))
	l_users.append(addUser(u"Наталья",u"Валерьевна",u"Коршакова","nkorshakova@uniwagon.com"))
	l_users.append(addUser(u"Евгения",u"Павловна",u"Прихидная","eprikhidnaya@uniwagon.com"))
	l_users.append(addUser(u"Антон",u"Николаевич",u"Панфилов","apanfilov@uniwagon.com"))
	l_users.append(addUser(u"Дмитрий",u"Николаевич",u"Панфилов","dpanfilov@uniwagon.com"))
	l_users.append(addUser(u"Кирилл",u"Викторович",u"Дьяконов","kdyakonov@uniwagon.com"))
	l_users.append(addUser(u"Никита",u"Викторович",u"Скоков","nskokov@uniwagon.com"))
	l_users.append(addUser(u"Зоя",u"",u"Ибрагимова","zibragimova@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Николаевна",u"Харитонова","okharitonova@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Игоревна",u"Смолькова","osmolkova@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Александровна",u"Сергеева","osergeeva@uniwagon.com"))
	l_users.append(addUser(u"Елизавета",u"Дмитриевна",u"Воронкова","evoronkova@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Николаевна",u"Шатова","oshatova@tt-center.ru"))
	l_users.append(addUser(u"Сергей",u"Викторович",u"Терехов","sterekhov@uniwagon.com"))
	l_users.append(addUser(u"Елена",u"Михайловна",u"Савельева","esavelyeva@uniwagon.com"))
	l_users.append(addUser(u"Светлана",u"Валентиновна",u"Соколова","ssokolova@uniwagon.com"))
	l_users.append(addUser(u"Евгения",u"Павловна",u"Прихидная","eprikhidnaya@uniwagon.com"))
	l_users.append(addUser(u"Рушана",u"Султановна",u"Калимуллина","rkalimullina@uniwagon.com"))
	l_users.append(addUser(u"Елена",u"Владимировна",u"Майер","Emayer@uniwagon.com"))
	l_users.append(addUser(u"Екатерина",u"Владимировна",u"Афонина","eafonina@uniwagon.com"))
	l_users.append(addUser(u"Евгений",u"Владимирович",u"Коновалов","ekonovalov@uniwagon.com"))
	l_users.append(addUser(u"Вадим",u"Викторович",u"Дубровский","vdubrovskiy@uniwagon.com"))
	l_users.append(addUser(u"Анна",u"Михайловна",u"Орлова","aorlova@uniwagon.com"))
	l_users.append(addUser(u"Андрей",u"Алексеевич",u"Кривченков","akrivchenkov@uniwagon.com"))
	l_users.append(addUser(u"Андрей",u"Геннадьевич",u"Цыганов","agtsyganov@uniwagon.com"))
	l_users.append(addUser(u"Андрей",u"Владимирович",u"Балашов","abalashov@uniwagon.com"))
	l_users.append(addUser(u"Ольга",u"Александровна",u"Сергеева","osergeeva@uniwagon.com"))
	l_users.append(addUser(u"Дарья",u"Петровна",u"Ножнова","dnozhnova@tt-center.ru"))
	l_users.append(addUser(u"Дмитрий",u"Александрович",u"Килуновский","dkilunovskiy@tt-center.ru"))
	l_users.append(addUser(u"Оксана",u"Николаевна",u"Гайдук","ogayduk@tt-center.ru"))
	l_users.append(addUser(u"Валерия",u"Олеговна",u"Лысяк","vlysyak@tt-center.ru"))
	l_users.append(addUser(u"Галина",u"Владимировна",u"Игнатова","gignatova@tt-center.ru"))
	l_users.append(addUser(u"Владимир",u"Павлович",u"Бахмат","vbakhmat@uniwagon.com"))
	l_users.append(addUser(u"Маргарита",u"Игоревна",u"Шлемина","mshlemina@tt-center.ru"))
	l_users.append(addUser(u"Надежда",u"Константиновна",u"Федорова","nfedorova@uniwagon.com"))
	l_users.append(addUser(u"Александр",u"Геннадьевич",u"Лебедев","alebedev@tt-center.ru"))
	l_users.append(addUser(u"Ирина",u"Васильевна",u"Бахмат","ibakhmat@tt-center.ru"))
	l_users.append(addUser(u"Дмитрий",u"Николаевич",u"Лосев","dlosev@uniwagon.com"))
	l_users.append(addUser(u"Алексей",u"Сергеевич",u"Тарасов","atarasov@uniwagon.com"))
	l_users.append(addUser(u"Руслан",u"Александрович",u"Фесюн","rfesyun@uniwagon.com"))
	l_users.append(addUser(u"Петр",u"Владимирович",u"Добрыднев","PDobrydnev@uniwagon.com"))
	l_users.append(addUser(u"Дмитрий",u"Александрович",u"Шитиков","dshitikov@tt-center.ru"))
	l_users.append(addUser(u"Леонид",u"Андреевич",u"Липилин","llipilin@uniwagon.com"))
	l_users.append(addUser(u"Юлия",u"",u"Лобанова","ylobanova@uniwagon.com"))
	l_users.append(addUser(u"Сергей",u"Николаевич",u"Яковенко","syakovenko@uniwagon.com"))
	l_users.append(addUser(u"Александр",u"Владимирович",u"Кульбицкий","akulbitskiy@uniwagon.com"))
	l_users.append(addUser(u"Олег",u"Николаевич",u"Спижевой","ospizhevoy@uniwagon.com"))
	l_users.append(addUser(u"Алексей",u"Евгеньевич",u"Бычков","abychkov@uniwagon.com"))
	l_users.append(addUser(u"Надежда",u"Анатольевна",u"Митрофанова","nmitrofanova@uniwagon.com"))
	l_users.append(addUser(u"Алексей",u"Владимирович",u"Коровкин","akorovkin@uniwagon.com"))
	l_users.append(addUser(u"Андрей",u"Викторович",u"Гусев","agusev@uniwagon.com"))
	l_users.append(addUser(u"Олеся",u"Владимировна",u"Войтова","ovoytova@uniwagon.com"))
	l_users.append(addUser(u"Вячеслав",u"Александрович",u"Виноградов","vvinogradov@uniwagon.com"))
	l_users.append(addUser(u"Евгений",u"Викторович",u"Шишов","eshishov@uniwagon.com"))
	l_users.append(addUser(u"Максим",u"Николаевич",u"Куземченко","mkuzemchenko@uniwagon.com"))
	l_users.append(addUser(u"Иван",u"Сергеевич",u"Лопарев","iloparev@uniwagon.com"))
	l_users.append(addUser(u"Игорь",u"Викторович",u"Илюхин","iilyukhin@uniwagon.com"))
	l_users.append(addUser(u"Олег",u"Викторович",u"Лысков","olyskov@uniwagon.com"))
	l_users.append(addUser(u"Анна",u"",u"Автухова","aavtukhova@uniwagon.com"))
	l_users.append(addUser(u"Иван",u"Владимирович",u"Поднебесный","ipodnebesnyi@uniwagon.com"))
	l_users.append(addUser(u"Виталий",u"Георгиевич",u"Антюхин","vantyukhin@uniwagon.com"))
	l_users.append(addUser(u"Виталий",u"Сергеевич",u"Муравьёв","vmuravyev@uniwagon.com"))
	l_users.append(addUser(u"Александра",u"Олеговна",u"Егорова","aegorova@uniwagon.com"))
	l_users.append(addUser(u"Роман",u"Владимирович",u"Лобанов","rlobanov@uniwagon.com"))
	l_users.append(addUser(u"Елена",u"Владимировна  ",u"Козлова","elkozlova@uniwagon.com"))
	l_users.append(addUser(u"Илья",u"Константинович",u"Ситников","isitnikov@uniwagon.com"))
	l_users.append(addUser(u"Светлана",u"Васильевна",u"Нармания","snarmania@uniwagon.com"))
	l_users.append(addUser(u"Сергей",u"Александрович",u"Котыш","kotysh@uniwagon.com"))
	l_users.append(addUser(u"Василий",u"Геннадьевич",u"Кузнецов","vkuznetsov@uniwagon.com"))
	l_users.append(addUser(u"Малика",u"Рашидовна",u"Тохчукова","mtokhchukova@tt-center.ru"))
	l_users.append(addUser(u"Олег",u"Аркадьевич",u"Бройтман","obroytman@tt-center.ru"))
	l_users.append(addUser(u"Денис",u"Владимирович",u"Шевченко","dshevchenko@tt-center.ru"))
	l_users.append(addUser(u"Александр",u"Евгеньевич",u"Филин","afilin@uniwagon.com"))
	l_users.append(addUser(u"Григорий",u"Юрьевич",u"Иванов","givanov@uniwagon.com"))
	l_users.append(addUser(u"Иван",u"Максимович",u"Гуков","igukov@uniwagon.com"))
	l_users.append(addUser(u"Евгений",u"Александрович",u"Щербаков","eshcherbakov@tt-center.ru"))
	l_users.append(addUser(u"Юрий",u"Анатольевич",u"Чумаков","ychumakov@uniwagon.com"))
	l_users.append(addUser(u"Константин",u"Игоревич",u"Рыжов","kryzhov@uniwagon.com"))
	l_users.append(addUser(u"Константин",u"Павлович",u"Дёмин","kdemin@uniwagon.com"))
	l_users.append(addUser(u"Алексей",u"Михайлович",u"Попков","apopkov@tt-center.ru"))
	l_users.append(addUser(u"Дмитрий",u"Вячеславович",u"Денисов","ddenisov@uniwagon.com"))
	l_users.append(addUser(u"Кирилл",u"Юрьевич",u"Попов","kpopov@uniwagon.com"))
	l_users.append(addUser(u"Станислав",u"Валентинович",u"Бутузов","sbutuzov@tt-center.ru"))
	l_users.append(addUser(u"Александр",u"Фёдорович",u"Албул","aalbul@tt-center.ru"))
	l_users.append(addUser(u"Александр",u"Николаевич",u"Васильев","avasilyev@tt-center.ru"))
	l_users.append(addUser(u"Дмитрий",u"Борисович",u"Денежкин","ddenezhkin@tt-center.ru"))
	l_users.append(addUser(u"Александр",u"Александрович",u"Сизов","asizov@tt-center.ru"))
	l_users.append(addUser(u"Анастасия",u"Евгеньевна",u"Хлыстова","akhlystova@tt-center.ru"))
	l_users.append(addUser(u"Денис",u"Александрович",u"Квактун","dkvaktun@tt-center.ru"))
	l_users.append(addUser(u"Кирилл",u"Александрович",u"Блинов","kblinov@tt-center.ru"))
	l_users.append(addUser(u"Александр",u"Леонидович",u"Ковязин","akovyazin@tt-center.ru"))
	l_users.append(addUser(u"Евгений",u"Геннадьевич",u"Пасько","epasko@tt-center.ru"))
	l_users.append(addUser(u"Тимофей",u"Сергеевич",u"Куклин","tkuklin@tt-center.ru"))
	l_users.append(addUser(u"Александр",u"Николаевич",u"Иванов","aivanov@tt-center.ru"))
	l_users.append(addUser(u"Михаил",u"Юрьевич",u"Тяжельников","mtyazhelnikov@tt-center.ru"))
	l_users.append(addUser(u"Татьяна",u"Владимировна",u"Босая","tbosaya@tt-center.ru"))
	l_users.append(addUser(u"Елена",u"Валерьевна",u"Кисон","ekison@tt-center.ru"))
	l_users.append(addUser(u"Макс",u"",u"Лукьяненко","macluk2204@gmail.com"))

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
#	u"Неопределено":"/img/noname_big.png",
#	u"Чехия":"/img/chehia_big.png",
#	u"Дания":"/img/dutch_big.png",
#	u"Англия":"/img/england_big.png",
#	u"Франция":"/img/france_big.png",
#	u"Германия":"/img/germany_big.png",
#	u"Греция":"/img/grecia_big.png",
#	u"Хорватия":"/img/horvatia_big.png",
#	u"Ирландия":"/img/irland_big.png",
#	u"Италия":"/img/italy_big.png",
#	u"Нидерланды":"/img/niderland_big.png",
#	u"Польша":"/img/polsha_big.png",
#	u"Португалия":"/img/portugal_big.png",
#	u"Россия":"/img/russia_big.png",
#	u"Швеция":"/img/shvec_big.png",
#	u"Испания":"/img/spain_big.png",
#	u"Украина":"/img/ukrain_big.png"}
	u"Неопределено":"",
	u"Бразилия"		:"flag-br",
	u"Хорватия"		:"flag-hr",
	u"Мексика"		:"flag-mx",
	u"Камерун"		:"flag-cm",

	u"Испания"		:"flag-es",
	u"Нидерланды"	:"flag-nl",
	u"Чили"			:"flag-cl",
	u"Австралия"	:"flag-au",

	u"Колумбия"		:"flag-co",
	u"Греция"		:"flag-gr",
	u"Кот-д’Ивуар"	:"flag-ci",
	u"Япония"		:"flag-jp",

	u"Уругвай"		:"flag-uy",
	u"Коста-Рика"	:"flag-cr",
	u"Англия"		:"flag-england",
	u"Италия"		:"flag-it",

	u"Швейцария"	:"flag-ch",
	u"Эквадор"		:"flag-ec",
	u"Франция"		:"flag-fr",
	u"Гондурас"		:"flag-hn",

	u"Аргентина"	:"flag-ar",
	u"Босния и Герцеговина"	:"flag-ba",
	u"Иран"			:"flag-ir",
	u"Нигерия"		:"flag-ng",

	u"Германия"		:"flag-de",
	u"Португалия"	:"flag-pt",
	u"Гана"			:"flag-gh",
	u"США"			:"flag-us ",

	u"Бельгия"		:"flag-be",
	u"Алжир"		:"flag-dz",
	u"Россия"		:"flag-ru",
	u"Корея"		:"flag-kr"
	}


	return t


