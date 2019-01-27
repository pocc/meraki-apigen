# -*- coding: utf-8 -*-
"""Test whether the API endpoints work per the sample requests provided."""
import subprocess as sp
import re
import time
import requests
import json

from _keys import api_key
from meraki_api_generator import get_meraki_apidocs_json, headers


def get_ids(widget_dict):
    """Get the list of IDs from an org or network dict."""
    return [widget['id'] for widget in widget_dict]


def eg_get_orgs():
    """Example function to verify that it's working."""
    resp = requests.get('https://api.meraki.com/api/v0/organizations',
                        headers=headers)
    return json.loads(resp.text)


def eg_get_networks(org_id=None):
    """Example to get networks."""
    if not org_id:
        org_id = eg_get_orgs()[0]['id']  # Get first org's ID
    resp = requests.get(
        'https://api.meraki.com/api/v0/'
        'organizations/{}/networks'.format(org_id),
        headers=headers)
    return json.loads(resp.text)


def test_api():
    """Test API GET calls."""
    org_id = eg_get_orgs()[0]['id']
    ntwk_id = eg_get_networks()[0]['id']
    api_json = get_meraki_apidocs_json()
    responses = {}
    for api_call in api_json:
        if api_call['http_method'] == 'GET':
            curl_sample = api_call['sample_req'].replace('<key>', str(api_key))
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


test_api()
