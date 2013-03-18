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
import datetime
import jinja2
import os
import logging
import json

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

now = datetime.datetime.now()

class Badge(ndb.Model):
    """Model for an individual badge"""
    badgeid = ndb.KeyProperty()
    name = ndb.StringProperty()
    version = ndb.StringProperty()
    description = ndb.StringProperty()


class BadgeAdminHandler(webapp2.RequestHandler):
    """Handles requests to view badge completion evidence for a specific user."""
    def get(self):
        logging.info('BadgeAdminHandler.get')
        badgeid = self.request.get('badgeid')

        if(badgeid):
            template = jinja_environment.get_template('/templates/badgeadmin.html')
            self.response.out.write(template.render())

    def post(self):
        logging.info('BadgeAdminHandler.post')

        try:
            badgeJson = self.request.get('badge')
            logging.info("badgeJson: " + badgeJson)
            badge = json.loads(badgeJson)
            self.response.out.write(badge)
        except Exception, e:
            logging.exception(e)

        
