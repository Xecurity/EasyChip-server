"""
    Copyright (C) 2012 Bo Zhu <zhu@xecurity.ca>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


import webapp2
import cgi
import json
import datastore
import gcm
#import urllib2

import logging
logging.getLogger().setLevel(logging.DEBUG)


class RegistrationHandler(webapp2.RequestHandler):
    def post(self):
        body_json = json.loads(cgi.escape(self.request.body))
        if 'email' not in body_json or 'reg_id' not in body_json:
            self.error(400)
            return
        email_addr = body_json['email']
        gcm_reg_id = body_json['reg_id']
        datastore.update(email_addr, gcm_reg_id)


class UnregistrationHandler(webapp2.RequestHandler):
    def post(self):
        body_json = json.loads(cgi.escape(self.request.body))
        if 'email' not in body_json or 'reg_id' not in body_json:
            self.error(400)
            return
        email_addr = body_json['email']
        gcm_reg_id = body_json['reg_id']
        datastore.delete(email_addr, gcm_reg_id)


class ChargeHandler(webapp2.RequestHandler):
    def post(self):
        body_json = json.loads(cgi.escape(self.request.body))
        email_addr = body_json['payer_email']
        gcm_reg_id = datastore.retrieve(email_addr)
        if gcm_reg_id:
            result, message = gcm.send(gcm_reg_id, body_json)
            if message:
                logging.debug(result + ': ' + message)
            else:
                logging.debug(result)
            if result == 'success':
                if message is not None:
                    gcm_reg_id = message
                    datastore.update(email_addr, gcm_reg_id)
                self.response.set_status(200)
                self.response.write('OK')
            else:
                self.response.set_status(500)
                self.response.write(message)
        else:
            self.response.set_status(402)
            self.response.write(
                    "Email Not Found. Might haven't installed the app!")


app = webapp2.WSGIApplication([
    ('/api/register', RegistrationHandler),
    ('/api/unregister', UnregistrationHandler),
    ('/api/charge', ChargeHandler),
], debug=True)
