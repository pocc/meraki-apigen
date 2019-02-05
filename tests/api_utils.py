# -*- coding: utf-8 -*-
# Copyright 2019 Ross Jacobs All Rights Reserved.
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
"""Toy python script to test various API functions."""
import subprocess as sp
import re
import time
import json

import requests

from merakygen._web import fetch_apidocs_json


with open('_vars.json') as myfile:
    JSON_VARS = json.loads(myfile.read())
API_KEY = JSON_VARS['API_KEY']
HEADERS = {
    'X-Cisco-Meraki-API-Key': API_KEY,
    'Content-Type': 'application/json'
}


def get_ids(widget_dict):
    """Get the list of IDs from an org or network dict."""
    return [widget['id'] for widget in widget_dict]


def eg_get_orgs():
    """Example function to verify that it's working."""
    resp = requests.get('https://api.meraki.com/api/v0/organizations',
                        headers=HEADERS)
    return json.loads(resp.text)


def eg_get_networks(org_id=None):
    """Example to get networks."""
    if not org_id:
        org_id = eg_get_orgs()[0]['id']  # Get first org's ID
    resp = requests.get(
        'https://api.meraki.com/api/v0/'
        'organizations/{}/networks'.format(org_id),
        headers=HEADERS)
    return json.loads(resp.text)


def save_apidocs_json_locally():
    """Save the APIdocs JSON to a file."""
    with open('api.json', 'w') as json_file:
        api_json = fetch_apidocs_json()
        # Add newline to beginning of each API call for readability.
        json_text = json.dumps(api_json).replace('{"http', '\n{"http')
        json_file.write(json_text)


def test_api():
    """Test API GET calls."""
    org_id = eg_get_orgs()[0]['id']
    ntwk_id = eg_get_networks()[0]['id']
    api_json = fetch_apidocs_json()
    responses = {}
    for api_call in api_json:
        if api_call['http_method'] == 'GET':
            curl_sample = api_call['sample_req'].replace('<key>', str(API_KEY))
            curl_sample = curl_sample.replace('[organization_id]', str(org_id))
            curl_sample = curl_sample.replace('[organizationId]', str(org_id))
            curl_sample = re.sub(r'organization/\[id\]',
                                 'organization/' + str(org_id), curl_sample)
            curl_sample = curl_sample.replace('[network_id]', str(ntwk_id))
            curl_sample = curl_sample.replace('[networkId]', str(ntwk_id))
            print(curl_sample)
            curl_cmd_list = get_cmd_list(curl_sample)
            # Remove any extraneous brackets
            curl_cmd_list[-1] = re.sub(r'[\[\]]', '', curl_cmd_list[-1])
            response = sp.Popen(curl_cmd_list).communicate()
            print("RESPONSE:", response)
            responses[api_call['description']] = response
            time.sleep(1)


def get_cmd_list(cmd_string):
    """ Get the command list from the command string.

    :param (str) cmd_string: curl commands to be parsed.
    :return: List of commands
    """
    # Skip splitting keys from values.
    cmd_string = cmd_string.replace(': ', ':')
    cmd_string = cmd_string.replace('\'', '')
    cmd_list = cmd_string.split(' ')
    print(cmd_list)

    return cmd_list
