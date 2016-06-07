#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import memcache
import random
import webapp2
import controller
import instl
import users
import football.admin.lists
import datetime
import string


class Tournaments(webapp2.RequestHandler):
	"""Описываем процедуры администрирования пользователей"""
	def get(self, idTournament=""):

		if (self.request.get('delete') == "true") :
			controller.deleteRound(idTournament)
			
			self.redirect(self.request.path[:-len(idTournament)] + "?msg=Раунд удален")
			return
		elif(self.request.get('action')=="delete_match"):

			self.deleteMatch(self.request.get('match'))

			self.redirect(self.request.path + "?msg=Матч удален")
			return

		elif (self.request.get('action')=="edit_match"):
			self.editMatch(idTournament, self.request.get('match'))
		else:
			self.performRequest(idTournament)
	pass

	def post(self, idTournament=""):

		if (self.request.get('action')=="edit"):
			self.changeTournament(idTournament)
		elif (self.request.get('action')=="match_complete"):
			self.completeMatch(idTournament)
		elif (self.request.get('action')=="add_match"):
			self.addMatch(idTournament)
		elif (self.request.get('action')=="change_match"):
			self.changeMatch(idTournament, self.request.get('match_key'))
		elif (self.request.get('action')=="edit_rate"):
			self.editRate(idTournament,self.request.get('rate'))
			pass

		self.performRequest(idTournament)
	pass


	def completeMatch(self, idTournament):
	
		r = self.request
		controller.completeMatch(
		idTournament, 
		r.get('match_key'), 
		r.get('left_value'), 
		r.get('right_value'),
		r.get('left_win_rate'),
		r.get('right_win_rate'),
		r.get('no_one_rate')
		)
		memcache.flush_all()

		pass

	def editRate(self  ,idTournament, rate):
		controller.editRate(idTournament, float(rate))
		pass

	def performRequest(self, idTournament = ""):

		template_values = {
		'title':u'Консоль администрирования',
		'title_page':u'Туры',
		'commands':controller.getCommands(),
		'navigation':football.admin.lists.getNavMenu("tournaments"),
		'navigation_tour': self.getTournamentsNavigation(idTournament),
		'matches':controller.getMatchesByTour(idTournament),
		'tour':controller.getRoundByKey(idTournament)}
	
		path = os.path.join(os.path.dirname(__file__), '../../../template/list/tournaments.html')
		self.response.out.write(template.render(path, template_values))

		#template = jinja_environment.get_template('../../../template/list/tournaments.html')	
		#self.response.out.write(template.render(template_values))

	pass
	def editMatch(self, idTournament, match_key):

		template_values = {
		'title':u'Консоль администрирования',
		'title_page':u'Туры',
		'commands':controller.getCommands(),
		'navigation':football.admin.lists.getNavMenu("tournaments"),
		'navigation_tour':self.getTournamentsNavigation(idTournament),
		'match': controller.getMatchView(match_key),
		'tour':controller.getRoundByKey(idTournament)}
	
		path = os.path.join(os.path.dirname(__file__), '../../../template/entities/match.html')
		self.response.out.write(template.render(path, template_values))

		#template = jinja_environment.get_template('../../../template/list/tournaments.html')	
		#self.response.out.write(template.render(template_values))

	pass

	def changeTournament(self, idTournament):
		"""Изменение параметров турнира"""


		tour = controller.getRoundByKey(idTournament)

		if (tour == {}) :
			return
		tour.title = self.request.get('name')
		tour.put()
		pass

	def addMatch(self, idTournament):
		"""Добавляем новый матч в турнир
		Параметры:
			daymatch	05.06
			group	Группа D
			leftcommand	95
			perform	add_match
			rightcommand	98
			timematch	16
		"""

		tour = controller.getRoundByKey(idTournament)
		if (tour == {}) :
			return


		new_match = {}
		new_match["tour"] = users.Rounds.get_by_id (long ( idTournament ) ).key
		new_match["firstCommand"] = users.Commands.get_by_id (long (self.request.get('leftcommand')) ).key
		new_match["secondCommand"] = users.Commands.get_by_id(long (self.request.get('rightcommand')) ).key
		new_match["group"] = self.request.get('group')
		new_match["matchTime"] = self.getDateTime(self.request.get('daymatch'),self.request.get('timematch'))

		controller.addMatch(new_match)
	pass

	def changeMatch(self, idTournament, key_match):
		"""Изменяем существующий матч"""

		new_match = users.Matches.get_by_id(long(key_match))
		new_match.firstCommand = controller.getCommandByID(self.request.get('leftcommand')).key
		new_match.secondCommand = controller.getCommandByID(self.request.get('rightcommand')).key
		new_match.group = self.request.get('group')
		new_match.matchTime = self.getDateTime(self.request.get('daymatch'),self.request.get('timematch'))

		new_match.put()






		pass


	def getDateTime(self, day_value, time_value):
		"""Определяем дату и время"""

		#определяем разделитель
		for d in day_value:
			if (not d in string.digits):
				split_value = d


		yyyy = 2012
		mm = 0

		# определяем дату 
		split_day = day_value.split(split_value)

		if (len(split_day)>1):
			dd = int(split_day[0])
			MMMM = int(split_day[1])
			if (len(split_day)>2):
				yyyy = int (split_day[2])

			if (yyyy < 2000):
				yyyy = yyyy+ 2000
		else:
			dd = 1
			MMMM = 1



		# определяем время

		split_time = time_value.split(":")

		hh = int (split_time[0])
		if (len (split_time) > 1):
			mm = int(split_time[1])


		"""  datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])"""

		return datetime.datetime(yyyy,MMMM,dd,hh,mm,0,0) - datetime.timedelta(hours=4)


		pass

	def deleteMatch(self,keyMatch):
		"""Удаляем матч"""

		controller.deleteMatch(keyMatch)
		pass



	def getTournamentsNavigation(self, idTournament):
		l = []
		for tour in controller.getRounds():
			l.append({'link':'/adminconsole/tournaments/'+ str(tour.key.id()) , 'title':tour.title , 'select': True if str(idTournament)==str(tour.key)  else False})
			pass
			
##		l.append({'link':'/adminconsole/tournaments/add', 'title':u"Новый Турнир" , 'select': "class='active'" if idTournament=="add"  else ""})
		return l
	pass




pass
