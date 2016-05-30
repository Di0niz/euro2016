#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
from google.appengine.ext.webapp import template
import webapp2
import random
import controller
import instl



class User(webapp2.RequestHandler):
	"""Описываем процедуры администрирования пользователей"""
	def get(self,values):
		if (self.request.get('delete') == "true") :
			controller.deleteUser(values)
			
			self.redirect(self.request.path[:-11] + "?msg=Пользователь удален")
			return
		self.performRequest(values)
	pass


	def post(self,values):

		if(self.request.get('perform') == "update") :

			fields ="lastName,firstName,secondName,company,mail"

			user = {}
			for field in fields.split(","):
				user[field] =  self.request.get(field) 

			controller.updateUser(values, user)

		self.performRequest(values)

	pass


	def performRequest(self, values):

		path = os.path.join(os.path.dirname(__file__), '../../template/entities/user.html')
		template_values = {'title':u'Консоль администрирования', 'user': controller.getUser(values)}
	
		self.response.out.write(template.render(path, template_values))

		pass


	pass

	pass
