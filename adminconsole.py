#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import random
import controller
import instl



class Propotype(webapp.RequestHandler):
	def get(self,values):
		self.performRequest(values)
	pass


	def post(self,values):


		newValue = None
		if (self.request.get('performaction') == "users_add"):

			fields ="surname,firstname,secondname,company,email"

			user = {}
			for field in fields.split(","):
				user[field] =  self.request.get(field) 

			# добавляем нового пользователя
			newValue = controller.addUser(user)

			pass


	#	self.response.out.write(self.request.arguments())

		self.performRequest(values,newValue)

	pass


	def performRequest(self, values, newValue=None):
		out = ""
		users_switch = False
		tournaments_switch = False
		commands_switch = False

		if ("users" in values):
			if "install" in values:
				instl.fillUsers()
				pass

			users_switch = True
			template_values = {"users":controller.getUsers()}

			path = os.path.join(os.path.dirname(__file__), 'template/users.html')
			out= template.render(path, template_values)

			pass
		elif("tournaments" in values):

			if "install" in values:
				instl.installMatches()
				pass



			tournaments_switch = True
			template_values = {"tournaments":controller.getTournaments()}

			path = os.path.join(os.path.dirname(__file__), 'template/tournaments.html')
			out= template.render(path, template_values)
			pass
		elif("commands" in values):
			if "install" in values:
				instl.installCommands()
				pass

			commands_switch = True
			template_values = {"commands":controller.getCommands()}

			path = os.path.join(os.path.dirname(__file__), 'template/commands.html')
			out= template.render(path, template_values)
			pass
		else:
			users_switch = True
			template_values = {"users":controller.getUsers()}

			path = os.path.join(os.path.dirname(__file__), 'template/users.html')
			out= template.render(path, template_values)

			pass

		template_values = {'logs':values, 
		'extern_table':out, 
		'users_switch':users_switch,
		'tournaments_switch':tournaments_switch,
		'commands_switch':commands_switch}
	
		path = os.path.join(os.path.dirname(__file__), 'template/adminconsole.html')

		self.response.out.write(template.render(path, template_values))

		pass


	pass

	def getTab(self):
	
		t  = ''

	pass
