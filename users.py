#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
#from google.appengine.ext import db
import datetime
import logging


class Users(ndb.Model):
	
	title = ndb.StringProperty()
	altTitle = ndb.StringProperty()
	firstName = ndb.StringProperty()
	lastName = ndb.StringProperty()
	secondName = ndb.StringProperty()

	company = ndb.StringProperty()
	mail = ndb.StringProperty()

	# определяем параметры ID
	idLink = ndb.StringProperty()

	# определяем дополнительные параметры
	agree = ndb.BooleanProperty()

	set_round = ndb.BooleanProperty()

	@classmethod
	def get_list (cls, keys_only=False, all_users=True):

		if all_users:
			q = cls.query().order(cls.title).fetch(200, keys_only=keys_only)
		else:
			q = cls.query(cls.set_round == True).order(cls.title).fetch(200, keys_only=keys_only)

		return q

	@classmethod
	def get_list_async (cls, keys_only=False, all_users=True):

		if all_users:
			q = cls.query().fetch_async(200, projection=["altTitle"])
		else:
			q = cls.query(cls.set_round == True).order(cls.title).fetch_async(200, keys_only=keys_only)

		return q

	@classmethod
	def get_auth_by_id (cls, id_auth):
		return cls.query().filter(cls.idLink==id_auth).fetch(1)
	
	pass

class Rounds(ndb.Model):

	title = ndb.StringProperty(required = True)
	rate = ndb.FloatProperty()
	order = ndb.IntegerProperty()

	@classmethod
	def get_list (cls):
		return cls.query().order(cls.order).fetch(10)
	
	@classmethod
	def get_list_async (cls):
		return cls.query().order(cls.order).fetch_async(10)

	@classmethod
	def get_dict (cls, key=None):
		d = {}
		for x in cls.get_list():
			if key == None:
				d[x.key.id()] = x
			else:
				d[x.title] = x.key

		return d

	@classmethod
	def get_current_tour(cls):

		res = Matches.query().filter(Matches.matchTime>datetime.datetime.today()).order(Matches.matchTime).fetch(1, projection=[Matches.tour])

		if (not res == []):
			return res[0].tour
		return None

	@classmethod
	def is_empty (cls, tour):

		res = Matches.query().filter(Matches.tour==tour).fetch(1, keys_only=True)
		return res==[]


class Commands(ndb.Model):
	name = ndb.StringProperty(required = True, indexed=True)
	css_class = ndb.StringProperty(indexed=False)
	bg_picture = ndb.StringProperty(indexed=False)
	small_picture = ndb.StringProperty(indexed=False)

	@classmethod
	def get_list (cls):
		return cls.query().order(cls.name).fetch(40)

	@classmethod
	def get_dict (cls, key=None):
		d = {}
		for x in cls.get_list():
			if key == None:
				d[x.key.id()] = x
			else:
				d[x.name] = x.key

		return d

	# определяем функцию по работе с асинхронными вызовами
	@classmethod
	def get_list_async(cls):
		return cls.query().order().fetch_async(40)


class Matches(ndb.Model):

	firstCommand		= ndb.KeyProperty(kind=Commands,indexed=False)
	secondCommand		= ndb.KeyProperty(kind=Commands,indexed=False)
	tour				= ndb.KeyProperty(kind=Rounds)
	group				= ndb.StringProperty()
	endTime				= ndb.StringProperty(indexed=False)
	matchTime			= ndb.DateTimeProperty()
	result				= ndb.StringProperty(indexed=False)
	left_value			= ndb.IntegerProperty(indexed=False)
	right_value			= ndb.IntegerProperty(indexed=False)
	left_win_rate   	= ndb.FloatProperty(indexed=False)
	right_win_rate 		= ndb.FloatProperty(indexed=False)
	no_one_rate			= ndb.FloatProperty(indexed=False)

	def match_time(self):
		"""Возвращаем время относительно часового пояса, используется 
		только для отображения"""

		return self.matchTime + datetime.timedelta(hours=4)

	def control_time(self):
		"""Время за 2 часа до матча, используется для контроля времени."""
		return self.matchTime - datetime.timedelta(hours=2)

	@classmethod
	def get_list (cls, tour=None, keys_only=False , sort_by_time = False):

		qr = Matches.query()
		if (tour is not None):
			qr = qr.filter(Matches.tour==tour)


		qr = qr.order(Matches.matchTime)

		return qr.fetch(200, keys_only=False)

	
	@classmethod
	def get_dict (cls, tour=None, keys_only=False , sort_by_time = False):
		d = {}
		for x in cls.get_list(tour = tour, keys_only=keys_only, sort_by_time=sort_by_time):
			if key == None:
				d[x.key.id()] = x
			else:
				d[x.name] = x.key

		return d


	@classmethod
	def get_list_async (cls, tour=None):
		if (tour == None):
			qr = cls.query()
		else:
			qr = cls.query(cls.tour==tour)

		return qr.fetch_async(200)

		

class UserRates(ndb.Model):
	user = ndb.KeyProperty(kind=Users)
	match = ndb.KeyProperty(kind=Matches)
	firstCommand = ndb.IntegerProperty(indexed=False)
	secondCommand = ndb.IntegerProperty(indexed=False)
	result = ndb.StringProperty(indexed=False)

	@classmethod
	def get_list (cls, user = None, key_matches = None):

		q = cls.query()
		if (not user==None):
			q = q.filter(UserRates.user==user)
		logging.info(key_matches)

		if (not (key_matches == None or key_matches == [])):
			q = q.filter (UserRates.match.IN ( key_matches) )

		return q.fetch(4000)


	@classmethod
	def get_list_async(cls, user = None, key_matches = None):

		q = cls.query()
		if (not user==None):
			q = q.filter(cls.user==user)

		if (not key_matches == None):
			q = q.filter (cls.match.IN ( key_matches) )

		return q.fetch_async(1100, batch_size=1100)		

	@classmethod
	def get_future_async(cls, approx_count = 1300 , user = None, key_matches = None):

		q = cls.query()
		if (not user==None):
			q = q.filter(cls.user==user)

		if (not key_matches == None):
			q = q.filter (cls.match.IN ( key_matches) )

		future_queries = []

		chunk = 300

		for i in range(0, approx_count, chunk):
			future_queries.append (q.fetch_async(300, offset=i))

		return future_queries 


class UserResults(ndb.Model):
	user = ndb.KeyProperty(kind=Users)
	match = ndb.KeyProperty(kind=Matches,indexed=False)
	order = ndb.IntegerProperty(indexed=False)

	@classmethod
	def get_list (cls):
		return cls.query().order(cls.user).fetch(4000)


	
