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
#import cgi
import webapp2
import datetime
#import urllib
import jinja2
import os
import logging
#import textwrap
import hashlib
import json

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

now = datetime.datetime.now()


class EvidenceHandler(webapp2.RequestHandler):
    """Handles requests to view badge completion evidence for a specific user."""
    def get(self):
        logging.info('EvidenceHandler.post')

        email = self.request.get('email')
        badgeid = self.request.get('badgeid')

        logging.info('Submitted values - [email=' + email + "], [badgeid='" + badgeid + "]")

        self.response.out.write("<h1>Badge Evidence (optional)</h1>")
        self.response.out.write("<b>Should contain information about how the specific Earner earned the badge.</b><br />")
        self.response.out.write("badge evidence for badgeid=" + badgeid + " and user=" + email + "<br />")


class CriteriaHandler(webapp2.RequestHandler):
    """Handles requests to view badge completion criteria."""
    def get(self, badgeid=0):
        template = jinja_environment.get_template('/templates/criteria.html')
        self.response.out.write(template.render({"badgeName": "BadgeName",
                                                 "badgeImageUrl": "http://mcbridebadgeissuer.appspot.com/images/badge0.png",
                                                 "description": "This is the badge description. It is an awesome badge. I hope many people earn it.",
                                                 "prerequisites": ["dog", "cat", "horse", "pig", "cow"]}))


class TestHandler(webapp2.RequestHandler):
    """Issues badges for testing purposes."""
    def get(self):
        template = jinja_environment.get_template('/templates/issuebadge.html')
        self.response.out.write(template.render())


class AssertionHandler(webapp2.RequestHandler):
    """Handles requests to view badge completion criteria."""
    def head(self):
        """Open Badge site requires support for HEAD and GET requests."""
        self.get()

    def get(self):
        email = self.request.get('email')
        badgeid = self.request.get('badgeid')

        logging.info('Submitted values - [email=' + email + "], [badgeid='" + badgeid + "]")

        id = int(badgeid or 0)
        if id > -1:

            indexOfController = self.request.url.rfind('/badge')
            url = self.request.url[:indexOfController]
            #logging.info('url: %s' % url)

            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

            #todo: get issuer/badge/assertion details from DB where appropriate
            issuerName = "KapX"
            issuerOriginUrl = "http://mcbridebadgeissuer.appspot.com"

            #todo: get badge details from DB.
            badgeVersion = "1.0"
            badgeName = "Test Badge " + badgeid
            imageUrl = url + "/images/badge" + badgeid + ".png"
            description = "This is test badge " + badgeid + " issued by a temporary OpenBadge issuer."
            criteriaUrl = url + "/criteria/" + badgeid

            uid = badgeid
            salt = "bad_salt"
            recipient = u'sha256${0}'.format(hashlib.sha256(email + salt).hexdigest())

            if id > -1 and id < 10:
                theIssuer = {'name': issuerName, 'origin': issuerOriginUrl}
                theBadge = {'version': badgeVersion, 'name': badgeName, 'image': imageUrl, 'description': description, 'criteria': criteriaUrl, 'issuer': theIssuer}
                theAssertion = {'uid': uid, 'recipient': recipient, 'salt': salt, 'badge': theBadge, 'issuer': theIssuer}

                self.response.out.write(json.dumps(theAssertion))

            else:
                self.response.out.write('{ "error":"badge id out of range supplied"}')

        else:
            self.response.out.write('{ "error":"invalid badge id supplied"}')
