#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
import controller

class BrowserHandler(webapp.RequestHandler):
	def get(self,projectNumber):
		template_values = {'game':projectNumber}


		path = os.path.join(os.path.dirname(__file__), 'template/game.html')

		self.response.out.write(template.render(path, template_values))

class RoundHandler(webapp.RequestHandler):
	def get(self,projectNumber, roundNumber):

		print controller.checkAndGetUser(self)

		template_values = {'game':projectNumber, 'round':roundNumber, 'progresses':self.generateRound()}

		path = os.path.join(os.path.dirname(__file__), 'template/round.html')

		self.response.out.write(template.render(path, template_values))

	def post(self,projectNumber, roundNumber):
		self.get(projectNumber, roundNumber)

	def generateRound(self):
		l = [ 
		{'progress': 20, 'rate':'1:3'},
		{'progress': 10, 'rate':'3:1'},
		{'progress': 30, 'rate':'5:3'},
		{'progress': 40, 'rate':'1:1'},
		{'progress': 10, 'rate':'0:0'}]

		return l





		



