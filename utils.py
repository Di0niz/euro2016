#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import string

def generateID(symbol_count) :

	"""Генерируем id для пользователей:
	- цифры
	- нижний регистр
	- верхний регистр"""


	genID = ""
	for i in range(0, symbol_count):

		switch_behaiver = int (random.random() *3)

		if (switch_behaiver == 0 ):

			symbol = "%d"%(int (random.random() *10))

		elif(switch_behaiver == 1):
			symbol = string.letters[int (random.random() *26)]

		elif(switch_behaiver == 2):
			symbol = string.letters[int (random.random() *26) + 26]

		pass

		genID = genID + symbol


		pass


	return genID

	pass


