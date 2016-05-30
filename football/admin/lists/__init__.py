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

from tournaments import Tournaments
from adjustments import Adjustments




def getNavMenu(currentElement = ""):

	"""Формируем список элементов меню"""

	l = []

	l.append({'link':'/adminconsole/users', 'title':u"Пользователи" , 'select': True if currentElement=="" or currentElement=="users" else False})
	l.append({'link':'/adminconsole/tournaments', 'title':u"Турниры", 'select': True if currentElement=="tournaments" else False})
	l.append({'link':'/adminconsole/commands', 'title':u"Команды", 'select': True if currentElement=="commands" else False})
	l.append({'link':'/adminconsole/setup', 'title':u"Настройки", 'select': True if currentElement=="setup" else False})

	return l
pass


__all__ = ['Tournaments','getNavMenu','Adjustments'] 