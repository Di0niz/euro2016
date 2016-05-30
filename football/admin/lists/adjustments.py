#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import random
import controller
import instl
import football.admin.lists
import datetime
import string
import instl


class Adjustments(webapp.RequestHandler):
	"""Описываем процедуры администрирования пользователей"""
	def get(self, command=""):


		commandName = self.request.get('action')
		if (commandName =="clear_user"):
			instl.clearUser()
		elif (commandName =="generate_brunswick"):
			instl.fillBrunswick()
		elif(commandName == 'delete_double'):
			instl.delete_double()



		self.performRequest(command)
	pass

	def post(self, command=""):

		commandName = self.request.get('action')

		if (commandName == 'generate_user'):
			instl.fillUsers()


		elif(commandName == 'generate_tour'):
			instl.installRounds()
			instl.installCommands()

		elif(commandName == 'generate_match'):

			instl.installMatches(0 if self.request.get('match_interval')=='' else int(self.request.get('match_interval')))



		self.performRequest(command)
	pass


	def performRequest(self, command = ""):

		path = os.path.join(os.path.dirname(__file__), '../../../template/list/install.html')


	
		template_values = {
		'title':u'Консоль администрирования',
		'title_page':u'Служебные параметры',
		'navigation':football.admin.lists.getNavMenu("setup")}
	
		self.response.out.write(template.render(path, template_values))

		pass


	pass




pass
