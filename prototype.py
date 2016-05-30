#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import random


class Propotype(webapp.RequestHandler):
	def get(self,projectNumber):
		template_values = {
		'game':projectNumber,
		'matches':self.matches(),
		'players':self.players(),
		'values':self.values()}

		path = os.path.join(os.path.dirname(__file__), 'template/prototype'+projectNumber+'.html')

		self.response.out.write(template.render(path, template_values))

		pass


	def players(self):

		l = []
		for i in range(1,60):
			l.append('Игрок ' + str(i))

		return l


	def matches(self):
		l = []


		l.append("Польша — Греция")
		l.append("Россия — Чехия")
		l.append("Греция — Чехия")
		l.append("Польша — Россия")
		l.append("Греция — Россия")
		l.append("Чехия — Польша")

		return l

	def values(self):

		l = []
		for m in self.matches():		
			for p in self.players():
				rand = random.randint(1,9) 
				className = "btn-inverse"
				if rand>6:
					className = "btn-success"
				elif rand>3:
					className = "btn-warning"


				l.append({'player':p, 'game':m, 'rate': rand,'className':className} )
		return l

	pass

