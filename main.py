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
import webapp2
from google.appengine.ext.webapp import util

import test 
import os
import browserhandler
import gamehandler
import prototype 
import logging 
import appengine_config

application = webapp2.WSGIApplication([('/', gamehandler.CurrentTourHandler),
(r'/game([\d])/round([\d]*).*', browserhandler.RoundHandler),
(r'/round([\d]+)/rate.*', gamehandler.RateHandler),
(r'/round([\d]+).*', gamehandler.RoundHandler),
(r'/final.*', gamehandler.FinalHandler),
(r'/common.*', gamehandler.CommonHandler),
(r'/auth_error.*', gamehandler.AuthErrorHandler),
(r'/game([\d])/round([\d]).*', browserhandler.RoundHandler),
(r'/game([\d]*)', browserhandler.BrowserHandler)],
debug=True)
