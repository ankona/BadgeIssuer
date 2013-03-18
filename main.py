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
import jinja2
import os
import badge
import badgeadmin

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

routes = [webapp2.Route('/test', badge.TestHandler),
          webapp2.Route('/assertion', badge.AssertionHandler),
          webapp2.Route('/criteria/<badgeid>', badge.CriteriaHandler),
          webapp2.Route('/evidence', badge.EvidenceHandler),
          webapp2.Route('/admin', badgeadmin.BadgeAdminHandler)]

app = webapp2.WSGIApplication(routes, debug=True)
