#!/usr/bin/env python

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

import json
import urllib2
from credentials import GCM_API_KEY


GCM_URL = 'https://android.googleapis.com/gcm/send'


# always send json to a single device
def send(single_registration_id, data_dict=None, collapse_key=None):
    headers = {
            'Authorization': 'key=' + GCM_API_KEY,
            'Content-Type': 'application/json'
    }

    body_dict = {'registration_ids': [str(single_registration_id)]}
    if collapse_key is not None:
        body_dict['collapse_key'] = str(collapse_key)
    if data_dict is not None:
        body_dict['data'] = data_dict
    data = json.dumps(body_dict)

    req = urllib2.Request(
            url=GCM_URL,
            headers=headers,
            data=data
    )

    try:
        resp = urllib2.urlopen(req).read()

    except urllib2.HTTPError as err:
        if err.code == 400:
            return 'failure', '400 JSON Error: ' + err.read()  # format errors
        elif err.code == 401:
            return 'failure', '401 Authentication Error'
        elif err.code == 500:
            return 'failure', '500 Google Internal Server Error'
        elif err.code == 503:
            return 'failure', '503 Google Server Temporarily Unavailable'
        else:
            err_body = err.read()
            if err_body:
                return 'failure', err_body
            else:
                return 'failure', str(err)

    except Exception as err:
        if hasattr(err, 'reason'):
            return 'failure', 'Internal Error: ' + str(err.reason)
        else:
            return 'failure', 'Internal Error: ' + str(err)

    resp_json = json.loads(resp)
    if resp_json['success'] == 1:
        if resp_json['canonical_ids'] == 0:
            return 'success', None
        else:
            # need to update the registration id in database
            return 'success', resp_json['results'][0]['registration_id']
    else:
        return 'failure', resp_json['results'][0]['error']


if __name__ == '__main__':
    reg_id = ''
    result, message = send(reg_id, {'message': 'test msg'})
    print result
    print message
