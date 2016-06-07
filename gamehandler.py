#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from google.appengine.ext import ndb
from google.appengine.api import memcache
import webapp2
import controller
import string
import datetime
import users
import data



def pageRender(out, template_values):

	path = os.path.join(os.path.dirname(__file__), 'template/main.html')

	out.write(template.render(path, template_values))

	pass


class TemplateHandler(object):

	def __init__(self):
		self.commands = None
		self.rounds = None
		self.matches = None
		self.users 	= None

	def createMenu(self, cur):

		l = memcache.get("menus")
		cur in '/common'

		if (l==None):
			l = []

			l.append({'title':u'Общая', 'link':'/common', 'active': None,'is_empty':False})

			for tour in self.get_rounds():

				is_empty = users.Rounds.is_empty(tour.key) # False #(res==[])

				link = '/round'+str(tour.key.id())
				l.append({'title':tour.title, 'link':link,'active':None, 'is_empty':is_empty})

			l.append({'title':u'Рейтинг', 'link':'/final', 'active':None, 'is_empty':False})

			memcache.add("menus", l, 3600)

		for x in l :
			x['active'] = cur in x['link']

		return l

		pass
	def checkAndGetUser(self, request):

		self.user = controller.checkAndGetUser(request)

		return self.user

	def template_add_user(handler, template):
		template['user'] =  handler.user 
		return template
	pass

	def template_add_title(self, template, title):
		template['title'] =  title
		return template
	pass

	def make_dic(self, query):
	 d = {}
	 for x in query:
	  d[x.key.id()] = x
	 return d

	def get_commands(self):
		if not 'commands'  in self.__dict__:
			self.commands = users.Commands.get_list()

		return self.commands 

	def get_rounds(self):

		mem_rounds = memcache.get("rounds")

		if (not mem_rounds == None):
			self.rounds = mem_rounds

		if not 'rounds' in self.__dict__ :
			self.rounds = users.Rounds.get_list()

		memcache.add ("rounds", self.rounds, 3600)

		return self.rounds 

	def get_matches(self, tour=None):
		if not 'matches' in  self.__dict__:
			self.matches = users.Matches.get_list(tour)

		return self.matches 

	def get_users(self, all_users):
		if not 'users' in self.__dict__:
			self.users = users.Users.get_list(all_users=all_users)

		return self.users 

	def template_add_matches(self, template, tour = None):

		time = datetime.datetime.today()
		commands_query  	= self.get_commands()
		match_query 		= self.get_matches (tour)

		commands_dic 		= self.make_dic(commands_query) # users.Commands.get_dict()

		key_matches = []

		template_matches = []

		for r_match in match_query:

			firCommand =		commands_dic[r_match.firstCommand.id()]
			secCommand =		commands_dic[r_match.secondCommand.id()]

			template_matches.append ({
				'left':				firCommand.name ,
				'left_img':			firCommand.bg_picture,

				'right':			secCommand.name,
				'right_img':		secCommand.bg_picture,
				
				'right_win_rate':   '' if r_match.right_win_rate == None else r_match.right_win_rate,
				'left_win_rate':    '' if r_match.left_win_rate == None else r_match.left_win_rate,
				'no_one_rate':		'' if r_match.no_one_rate == None else r_match.no_one_rate,

				'time':				r_match.match_time().strftime("%d.%m %H:%M"), # %y
				'result':			' ' if r_match.result == None else r_match.result,
				'is_result': 		False if r_match.left_value == None or r_match.right_value ==None else True,
				'isEnd': 			(time > r_match.match_time())
			})

			#key_matches.append(match.key.)

		template['matches'] = template_matches

		template_rates = []

		all_total = 0.0

		user_rates_query 	= users.UserRates.get_list ()
		users_query 		= self.get_users(all_users=False) 

		for u in users_query:
			user_key = u.key

			user = {'title':u.title}


			# рассчитываем тотал
			total = 0.0
			for m in match_query:

				is_match_complete = False if m.left_value == None or m.right_value ==None else True

				key_id = m.key

				rate = {} # getRate(user,user_key, key_id, match_results, is_match_complete)

				result = self.get_user_rates (user_rates_query, user_key, key_id)
				if not result == None: # user_key in user_rates_query and match_key in match_results[user_key]:
					#result = match_results[user_key][match_key]

					rate = {
					'user'		:	user,
					'is_rate'	: 	False if result.firstCommand == None or result.secondCommand == None else True, 
					'left'		: 	result.firstCommand, 
					'right'		:	result.secondCommand, 
					'result'	:	result.result,
					'is_result'	:	is_match_complete
					}
				else:
					rate = {
					'user'		:	user,
					'is_rate'	: 	False,
					'is_result'	: 	is_match_complete,
					'result'	:	0.0
					}

				template_rates.append(rate)

				# расчитываем тотал
				total = total + (0.0 if rate['result'] =='' or rate['result'] == None else float(rate['result']))


			user['total'] = total
			all_total = all_total + total

	#		print (user)


		#template['user']['total'] = template_total
		template['is_total'] = not( all_total == 0.0 ) # определяем есть ли колонка итого

		template['rates'] = template_rates
	#	print ("template_rates: %s" % template_rates)

		return template
	pass

	def get_user_rates (self, user_rates_query, user_key, match_key):
		l = [x for x in user_rates_query if x.user==user_key and x.match==match_key]
		if l==[]:
			return None
		return l [0]

	def getMatch(self, r_match, l_commands, time):

		firstCommand =l_commands[long(users.Matches.firstCommand.get_value_for_datastore(r_match).id())]
		secondCommand = l_commands[long(users.Matches.secondCommand.get_value_for_datastore(r_match).id())]

		t = {
		'left'				: firstCommand['title'],
		'right'				: secondCommand['title'],
		'left_img'			: firstCommand['img'],
		'right_img'			: secondCommand['img'],
		'time'				: r_match.match_time().strftime("%d.%m %H:%M"), # %y
		'result'			: ' ' if r_match.result == None else r_match.result,
		'is_result'			: False if r_match.left_value == None or r_match.right_value ==None else True,
		'isEnd'				: (time > r_match.match_time())
		}
		
		return t

	pass

	def getRate(self, user, user_key, match_key, match_results, is_complete):



		if user_key in match_results and match_key in match_results[user_key]:
			result = match_results[user_key][match_key]

			t = {
			'user'			: user,
			'is_rate'		: True, 
			'left'			: result['left'], 
			'right'			: result['right'], 
			'result'		: result['result'],
			'is_result'		: result['is_result']
			}
		else:
			t = {
			'user' 			: user,
			'is_rate' 		: False,
			'is_result' 	: is_complete,
			'result' 		: 0.0
			}
		return t
	pass

	def get_match_result(self, user_key, match_key, match_results):

		return 0.0
		if user_key in match_results and match_key in match_results[user_key]:
			result = match_results[user_key][match_key]
			return 0.0 if result['result']=='' else float(result['result'])
		else:
			return 0.0

	pass

	def getTotal(self, user_key, total):

		return {'total':total}
	pass


	def template_add_menu(self, template, title):
		template['menu_list'] = self.createMenu(title)
		return template
	pass

	def template_add_custom(self, template, title, value):
		template[title]=value
		return template
	pass

	def template_add_rates(self, template):

		mem_final_table = memcache.get("rates")
		if mem_final_table is not None:
			template['rates'] = mem_final_table
			return template
	
		# определяем пользователей

		#commands_query  	= users.Commands.get_list()
		match_query 		= self.get_matches ()
		round_query 		= self.get_rounds ()
		user_query 			= self.get_users (all_users=False)
		user_result			= users.UserRates.get_list()

		rating_map = {}

		final_table = []

		for user in user_query:

			user_title = user.title
			grand_total = 0.0

			results = []

			for tour in round_query:

				
				total = 0.0

				for m in [m for m in match_query if m.tour == tour.key]:

					# считаем тотал
					for res in [res for res in user_result if res.user == user.key and res.match == m.key]:
						total = total +  (0.0 if res.result == None else float(res.result)) 

				grand_total = grand_total + total

				results.append (total)

			item = {'title':user_title, 'rate_index':0, 'results':results, 'total':grand_total}

			final_table.append(item)

		# сортируем таблицу по результату
		final_table = sorted(final_table, key=lambda k: (-k['total']))

		rate_index = 0
		prev_value = None
		for x in final_table:
			if (not prev_value == x['total']):
				rate_index = rate_index + 1
			prev_value = x['total']
			x['rate_index'] = rate_index

		memcache.add("rates", final_table, 3600)

		template['rates'] = final_table

		return template
	pass



class RoundHandler(webapp2.RequestHandler,TemplateHandler):
	def get(self,projectNumber):

		r = controller.getRound(projectNumber)
		super(RoundHandler, self).checkAndGetUser(self)

		template_values = {}
		super(RoundHandler, self).template_add_user(template_values)
		super(RoundHandler, self).template_add_title(template_values, r.title)
		super(RoundHandler, self).template_add_menu(template_values, 'round%s'%projectNumber)
		
		super(RoundHandler, self).template_add_matches(template_values, r.key)
		
		super(RoundHandler, self).template_add_custom(template_values,'round',projectNumber)
		super(RoundHandler, self).template_add_custom(template_values,'is_common',template_values['user']==None)
		
#		u =  controller.checkAndGetUser(self)

		#template_values = {"round":controller.getRates()}
		templateName = 'template/round.html'



		#template_values = {
		#'user':u,
		#'title':r.title,
		#'matches':controller.getMatches(r.key), 
		#'rates':controller.getMatchRates(r.key), 
		#'menu_list':createMenu('round%s'%projectNumber), 
		#'round':projectNumber	}

		path = os.path.join(os.path.dirname(__file__), templateName)

		self.response.out.write(template.render(path, template_values))
	pass
pass

class CommonHandler(webapp2.RequestHandler,TemplateHandler):
	def get(self):

		template_values = {}
		super(CommonHandler, self).checkAndGetUser(self)
		
		super(CommonHandler, self).template_add_user(template_values)
		super(CommonHandler, self).template_add_title(template_values, u"Общая таблица")
		super(CommonHandler, self).template_add_menu(template_values, 'common')
		super(CommonHandler, self).template_add_matches(template_values)
		super(CommonHandler, self).template_add_custom(template_values,'is_common',True)

		path = os.path.join(os.path.dirname(__file__), 'template/round.html')

		self.response.out.write(template.render(path, template_values))
	pass
pass

class CurrentTourHandler(webapp2.RequestHandler,TemplateHandler):
	def get(self):

		u =  controller.checkAndGetUser(self)

		current_tour = controller.get_current_tour()

		auth_link = ""
		if (not self.request.get('auth')==''):
			auth_link = "?auth=" + self.request.get('auth')

		if (current_tour == None):
			self.redirect("/common" + auth_link)
		else:
			self.redirect("/round" + str(current_tour.id()) + auth_link)
	pass
pass

class AuthErrorHandler(webapp2.RequestHandler):
	def get(self):

		template_values = {}

		path = os.path.join(os.path.dirname(__file__), 'template/auth_error.html')

		self.response.out.write(template.render(path, template_values))
	
	pass
pass

class RateHandler(webapp2.RequestHandler, TemplateHandler):
	def get(self,projectNumber):

		u = super(RateHandler, self).checkAndGetUser(self)
		# u =  controller.checkAndGetUser(self)

		r = controller.getRound(projectNumber)

		matches = controller.getMatchesByGroup(u,r.key)

		#user_rates = controller.getUserRates(projectNumber, u)

		template_values = {
		'title'		: u"Сделать прогноз",
		'user'		: u,		
		'tour'		: {'id'		:r.key.id()}, 
		'matches'	: matches, 
		'menu_list'	: super(RateHandler, self).createMenu(u'round%s'%projectNumber)
		}
		path = os.path.join(os.path.dirname(__file__), 'template/rate.html')

		self.response.out.write(template.render(path, template_values))

		pass
	def post (self, projectNumber):

		u =  controller.checkAndGetUser(self)

		if (not u.set_round == True):
			u.set_round = True
			u.put()

		m = {}
		for var in self.request.arguments():
			if u"match_" in var :

				key = var.split("_")[1]

				if not key in m:
					m[key] = {'left':'','right':''}
				if "left" in var:
					m[key]['left'] = self.request.get(var)
				if "right" in var:
					m[key]['right'] = self.request.get(var)
			pass
		pass


		# перебираем полученные результаты матчей
		
		t = datetime.datetime.today()

		user_rates = []
		delete_user_rates = []
		for id_match in m:
			match = controller.getMatch(id_match)

			# не изменяем ставку, после того, как время истекло
			if (match.control_time() < t):
				continue

			entity = controller.getUserRates(u, match)

			entity.firstCommand = None if (m[id_match]['left'] == "") else int(m[id_match]['left'])
			entity.secondCommand = None if (m[id_match]['right'] == "") else int(m[id_match]['right'])
#				entity.result = "%s : %s " % ("0" if (m[id_match]['left'] == "") else m[id_match]['left'], "0" if (m[id_match]['right'] == "")else m[id_match]['right']) 

			# устанавливаем 0, если указано только одно из значений
			entity.firstCommand = 0 if entity.firstCommand == None and not entity.secondCommand == None else entity.firstCommand 
			entity.secondCommand = 0 if entity.secondCommand == None and not entity.firstCommand == None else entity.secondCommand

			user_rates.append(entity)

		controller.updateUserRates(user_rates)

			# for id_match in m:


		self.redirect(self.request.path[:-4])


class FinalHandler(webapp2.RequestHandler,TemplateHandler):
	def get(self):

		super(FinalHandler, self).checkAndGetUser(self)

		template_values = {}

		super(FinalHandler, self).template_add_user(template_values)
		super(FinalHandler, self).template_add_title(template_values, u"Рейтинг")
		super(FinalHandler, self).template_add_menu(template_values, 'final')
		super(FinalHandler, self).template_add_rates(template_values)
		super(FinalHandler, self).template_add_custom(template_values,'is_common',True)


		path = os.path.join(os.path.dirname(__file__), 'template/rates.html')

		self.response.out.write(template.render(path, template_values))


