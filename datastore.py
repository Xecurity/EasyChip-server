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


from google.appengine.ext import db


class DeviceRecord(db.Model):
    # to use email_addr as the unique user id
    # email_addr = db.db.EmailProperty(required=True)
    gcm_reg_id = db.TextProperty(required=True)  # Text is not indexed


def retrieve(email_addr):
    entry_key = db.Key.from_path('DeviceRecord', email_addr)
    entry_class = db.get(entry_key)
    if entry_class:
        return entry_class.gcm_reg_id
    else:
        return None


def update(email_addr, gcm_reg_id):
    entry_class = DeviceRecord(key_name=email_addr, gcm_reg_id=gcm_reg_id)
    entry_class.put()


def delete(email_addr, gcm_reg_id):
    entry_key = db.Key.from_path('DeviceRecord', email_addr)
    entry_class = db.get(entry_key)
    if entry_class and entry_class.gcm_reg_id == gcm_reg_id:
        db.delete(entry_key)
