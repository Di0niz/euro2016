#!/usr/bin/env python
# -*- coding: utf-8 -*-

import users
import utils
from google.appengine.ext.ndb import Key
from google.appengine.ext import ndb

def getRounds(keys_only=False):

	results = users.Rounds.get_list() 
	return results


	pass
def getRoundByKey(key):
	return users.Rounds.get_by_id(long(key))
pass

def getMatch(id_match):
	return users.Matches.get_by_id(long(id_match))
pass

def getUserRates(u,m):

	res =  users.UserRates.get_list(u.key,  [m.key])

	if not res == [] :
		entity = res[0]
		entity.key.delete()

	entity = users.UserRates()
	entity.user 		 = u.key
	entity.match  		 = m.key

	return entity

pass


def getUsers(keys_only=False):
	#config = ndb.create_config(deadline=5, read_policy=ndb.EVENTUAL_CONSISTENCY)
	#results = users.Users.gql("ORDER BY title").run(config=config)


	results = users.Users.query().order(users.Users.title).fetch(200,keys_only=keys_only)
	#return []
	return results

	pass


def getUser(idLink):

	return users.Users.gql("WHERE idLink=:1", idLink)[0]
	pass

def getMatches(tour=None, orderBy="",keys_only=False):

	return users.Matches.get_list(tour, keys_only)

	pass

def addUser(newUser):

	if (newUser['firstname'] == None):
		title = newUser['surname']
	elif (newUser['secondname'] == ''):
		title = "%s %s." % (newUser['surname'],  newUser['firstname'][0])
	else:
		title = "%s %s.%s." % (newUser['surname'],  newUser['firstname'][0] , newUser['secondname'][0])

	entity = users.Users()
	entity.title = title

	title = newUser['surname']
	
	if (newUser['secondname'] == ''):
		entity.altTitle = "%s" % (newUser['firstname'])
	else:
		entity.altTitle = "%s %s" % (newUser['firstname'],  newUser['secondname'])

	entity.lastName = newUser['surname']
	entity.firstName = newUser['firstname']
	if (newUser['secondname'] == None):
		entity.secondName = ''
	else:
		entity.secondName = newUser['secondname']

	entity.company = newUser['company']
	entity.mail = newUser['email']

	entity.idLink = utils.generateID(10)

	entity.put()


	return entity

	pass

def getMatchByKey(key_value):
	return users.Matches.get_by_id(long(key_value))

	pass

def addMatch(newMatch):

	entity = users.Matches()

	entity.firstCommand 	= newMatch['firstCommand']
	entity.secondCommand 	= newMatch['secondCommand']
	entity.tour 			= newMatch['tour']
	entity.group 			= newMatch['group']
	#entity.endTime = newMatch['endTime']
	entity.matchTime 		= newMatch['matchTime']


	entity.put()

	return entity

	return
	pass



def updateUser(idLink, newUser):

	if newUser['firstName'] =='':
		title = newUser['lastName']
	elif newUser['secondName']=='':
		title = "%s %s." % (newUser['lastName'],  newUser['firstName'][0])
	else:
		title = "%s %s.%s" % (newUser['lastName'],  newUser['firstName'][0] , newUser['secondName'][0])

	entity = getUser(idLink)
	entity.title = title

	if (newUser['secondName'] == ''):
		entity.altTitle = "%s" % (newUser['firstName'])
	else:
		entity.altTitle = "%s %s" % (newUser['firstName'],  newUser['secondName'])

	entity.lastName = newUser['lastName']
	entity.firstName = newUser['firstName']
	if (newUser['secondName'] == ''):
		entity.secondName = ''
	else:
		entity.secondName = newUser['secondName']

	entity.company = newUser['company']
	entity.mail = newUser['mail']
	
	entity.put()


	return entity

	pass

def getCommands():

	"""Получаем список команд"""
	return users.Commands.all()


pass


def getCommandByID(idCommand):
	"""Получаем команду по уникальному идентификатору"""
	res =  users.Commands.get_by_id(long(idCommand))
	return res
	pass


def getRound(tour, key_only = False):
	"""Получаем матч по названию"""

	key = None
	if key_only==True:
		key = ndb.Key("Rounds", long(tour))
	else:
		results = users.Rounds.get_by_id(long(tour))
		key = results

	return key

	pass


	
def getUserByAuth(id_auth):

	if (id_auth == None):
		return None

	results = users.Users.get_auth_by_id(id_auth)	
	#list_users = users.Users.gql("WHERE idLink=:1", id_auth)

	if (len(results) == 0):
		return None
	return results[0]

	pass



