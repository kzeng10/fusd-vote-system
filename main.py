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
#lqdqhxmlrkarcczq

import webapp2
import re
from speak import AdminHandler, LoginHandler, SpeakHandler, JSONHandler

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(file('landing.html', 'r').read())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/admin', AdminHandler),
    ('/login', LoginHandler),
    ('/speak', SpeakHandler),
    ('/json', JSONHandler)
], debug=True)
