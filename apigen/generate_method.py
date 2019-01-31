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
"""Get various variables for funtion text."""
import re
import datetime
import collections
import textwrap

import inflection as inf

from apigen import __version__ as apigen_version

BASE_URL = 'https://api.meraki.com/api/v0'
API_PRIMITIVES = {
    'org_id': '(eg 212406)' + '\n' + 12*' ' + '↳ get_orgs()',
    'network_id': '(eg N_24329156)' + '\n' + 12*' ' +
                  '↳ get_networks_by_org_id(org_id)',
    'admin_id': '(eg 545173)' +
                '\n' + 12*' ' + '↳  get_admins_by_org_id(org_id)',
    'sr_id': 'Static route ID like d7fa4948-7921-4dfa-af6b-ae8b16c20c39\n' +
             12*' ' + '↳ get_static_routes_by_network_id(network_id)',
    'serial': 'Serial# of a device (eg Q234-ABCD-5678)\n' + 12*' ' +
              '↳ get_devices_by_network_id(network_id)',
    'named_tag_scope_id': 'Tag SM scope ID (eg 1234)\n' + 12*' ' +
                          '↳ get_sm_named_tag_scopes_by_network_id'
                          '(network_id, params)',
    'user_id': 'User ID used for SM (eg 1284392014819)\n' + 12*' ' +
               '↳ get_sm_users_by_network_id(network_id, params)',
    'ssid_number': 'Positional number of the SSID in the list (0-14)\n' +
                   12*' ' + '↳ get_ssids_by_network_id(network_id)',
    'zone_id': 'Camera Analytics Zone ID'
               '\n' + 12*' ' + '↳ get_analytics_zones_by_serial(serial)',
    'bluetooth_client_id': 'Bluetooth MAC (eg 00:11:22:33:44:55)\n' + 12*' ' +
                           '↳ get_bluetooth_clients_by_network_id'
                           '(network_id, params)',
    'id_or_mac_or_ip': 'Client ID or Mac or IP\n' + 12*' ' + '↳',
    'mac': 'Client MAC\n' + 12*' ' +
           '↳ get_clients_by_serial(serial, params)',
    'config_template_id': '(eg N_24329156)\n' + 12*' ' +
                          '↳ get_config_templates_by_org_id(org_id)',
    'http_server_id': 'Webhook HTTP server ID. See'
                      '\n' + 16*' ' + 'https://documentation.meraki.com/z'
                      '\n' + 16*' ' + 'General_Administration/Other_Topics/'
                      'Webhooks\n' + 12*' ' +
                      '↳ get_http_servers_by_network_id(network_id)',
    'webhook_test_id': 'ID of webhook test sent to your HTTP server. See'
                       '\n' + 16*' ' + 'https://documentation.meraki.com/z'
                       '\n' + 16*' ' + 'General_Administration/Other_Topics/'
                       'Webhooks\n' + 12*' ' +
                       '↳ create_http_servers_webhook_tests_by_network_id('
                       '\n' + 16*' ' + 'network_id, params)',
    'meraki_auth_user_id': 'Splash or RADIUS user hash (eg aGlAaGkuY29t)' +
                           '\n' + 12*' ' + '↳ get_meraki_auth_users_by_'
                           'network_id(network_id)',
    'phone_announcement_id': 'Announcement ID (eg 1284392014819)'
                             '\n' + 12*' ' + '↳ get_phone_' +
                             'announcements_by_network_id(network_id)',
    'phone_callgroup_id': 'Callgroup ID (eg 178449602133687616)'
                          '\n' + 12*' ' + '↳ '
                          'get_phone_callgroups_by_network_id(network_id)',
    'phone_conference_room_id': 'Room ID (eg 563512903374733359)'
                                '\n' + 12*' ' + '↳ get_networks_'
                                'by_org_id(org_id)',
    'contact_id': 'Phone contact ID (eg 823)' + '\n' + 12*' ' +
                  '↳ get_phone_assignments_by_network_id(network_id)',
    'request_id': 'PII request ID (eg 1234)' + '\n' + 12*' ' +
                  '↳ get_pii_requests_by_network_id(network_id)',
    'saml_role_id': 'ID unique to SAML User (eg TEdJIEN1c3RvbWVy)\n' + 12*' ' +
                    '↳ get_saml_roles_by_org_id(org_id)',
    'client_id': 'Client ID Hash (eg k74272e)\n' + 12*' ' +
                 '↳ get_clients_by_serial(serial)',
    'profile_id': 'Cisco Clarity Profile ID (eg 12345)' + '\n' + 12*' ' +
                  '↳ create_profile_clarity_by_network_id(network_id, params)',
    'app_id': 'SM Cisco Polaris app ID (eg 123456)\n' + 12*' ' +
              '↳ get_app_polaris_by_network_id(network_id, params)',
    'sm_id': '???\n' + 12*' ' + '↳ ???',
    'service': 'MX Services (eg \'web\')\n' + 12*' ' +
               '↳ get_firewalled_services_by_network_id(network_id)',
    'vlan_id': 'VLAN number (eg 1234)' +
               '\n' + 12*' ' + '↳ get_vlans_by_network_id(network_id)',
    'switch_port_number': 'like (1-48)\n' + 12*' ' +
                          '↳ get_switch_ports_by_serial(serial)',
    'target_group_id': 'Beta endpoint lacks means of fetching ID.' +
                       '\n' + 12*' ' + '↳ get_switch_ports_by_serial(serial)',

    'params': 'Dict of params passed'
}


def get_http_stats(api_calls):
    """Per the API calls, get the number of each http type (GET, POST, ...)"""
    http_types_list = [api_call['http_method'] for api_call in api_calls]
    http_types_counts = dict(collections.Counter(http_types_list))
    return re.sub(r'[\']', '', str(http_types_counts))


def get_preamble(cli_options, num_api_calls, http_stats, lang):
    """Generate the docstring header at the top of the file."""
    date = datetime.datetime.now().isoformat()
    options_str = ' '.join(cli_options)
    header = """Generated and linted at {}
Using:  meraki-apigen --key <key> {}
Pulled data from Meraki API v0 (https://dashboard.meraki.com/api_docs/)
API calls: {} {}

Meraki API Generator v{}
    Convert all Meraki API calls into [{}] function calls.
    As new API calls are released all the time, rerun this occasionally.

More Info
    Author: Ross Jacobs (rosjacob [AT] cisco.com)
    Github: https://github.com/pocc/meraki-apigen
    Issues: https://github.com/pocc/meraki-apigen/issues
""".format(date, options_str, num_api_calls, http_stats, apigen_version, lang)
    return header


def get_path_args(api_path, has_params):
    """Get all of the arguments for a function

    In a path, sometimes [networkId] or [organizationId] is just [id].
    Change [id] to the correct longer form. Then get all as parameters.
    """
    # Replace /variable/id wih /variable_id
    api_path = re.sub(r'/([A-Za-z_]*?)/\[id\]', r'/[\1_id]', api_path)
    # Get everything in [brackets] in url.
    args = re.findall(r'[\[{]([A-Za-z_]*)[\]}]', api_path) or []

    for index, arg in enumerate(args):
        if 'organization' in arg:
            arg = arg.replace('organization', 'org')
        if arg == 'number':
            arg = re.findall(r'\/([A-Za-z-_]*?)\/\[number\]', api_path)[0]
            arg += '_number'
        if 's_' in arg:  # Remove needless plurals
            arg = arg.replace('s_', '_')
        args[index] = inf.underscore(arg)

    if has_params:
        args += ['params']

    return args


def get_formatted_url(api_call_path, has_params):
    """Format the URL string for use in the end function.

    Get the URL string such that parameters passed in can be sent in the
    request by adding them with string.format() in the end function."""
    # The variables that will end up being in the function
    func_vars = ', '.join(get_path_args(api_call_path, has_params))
    func_vars = inf.underscore(func_vars)
    temp_path = re.sub(r'[\[{][A-Za-z_-]*[\]}]', '{}', api_call_path)

    formatted_path = "'{}'.format({})".format(temp_path, func_vars)
    return formatted_path


def generate_api_call_name(http_type, api_path):
    """Generate the API call name as a unique one is not provided."""
    # Use 'create' and 'update' instead of 'post' and 'put' for readability.
    http_type = http_type.replace('POST', 'create').replace('PUT', 'update')
    http_type = http_type.lower()
    api_path = api_path.replace('organization', 'org')
    path_words = list(filter(None, api_path.split('/')))

    word_list = []
    for i, word in enumerate(path_words[::-1]):
        if word == '[srId]':  # Static route ID
            word = '[id]'
        if word == '[service]':  # For FirewalledServices [service] variable
            word = '[type]'
        word = inf.underscore(word)
        is_get = http_type in ['get']
        if not is_get and 'settings' not in word:
            word = inf.singularize(word)
        if word[0] in ['[', '{']:
            word = word[1:-1]
            # First word is never [arg]
            word_before = path_words[::-1][i+1]
            word_before = inf.singularize(inf.underscore(word_before))
            # Combines /networks/[networkId] => networkId
            if word_before not in word:
                word = word_before + '_' + word
            if i == 0:
                if is_get:
                    word_before = inf.pluralize(word_before)
                return http_type + '_' + word_before + '_by_' + word
            if i > 0:
                if not is_get and 'settings' not in word_list[-1]:
                    word_list[-1] = inf.singularize(word_list[-1])
                word_list.insert(0, http_type)
                return '_'.join(word_list) + '_by_' + word
        word_list.insert(0, word)

    return http_type + '_' + '_'.join(word_list)


def remove_html(target_string):
    """Remove HTML tags from a string."""
    target_string = re.sub(r'<a[\s\S]*?href=[\'\"]', '', target_string)
    return re.sub(r'[\'\"][\s\S]*?a>', '', target_string)


def get_function_parts(api_call, func_args, options):
    """Get the function description."""
    class_indent = bool('classy' not in options) * 4  # Classes need indent
    recommended_width = 68 + class_indent

    func_param_descs = []
    has_params = 'params' in api_call and api_call['params']
    func_desc = get_func_description(api_call, recommended_width, func_args)
    if has_params:
        func_param_descs.append('\n\n    Params: (dict)')
        for param in api_call['params']:
            param['description'] = remove_html(param['description'])
            func_param_descs.append('\n        - ' + param['name'] + ': '
                                    + param['description'])
    if func_param_descs and len(max(func_param_descs, key=len)) > 75:
        for idx, desc in enumerate(func_param_descs):
            # Add each wrapped line to the desc param list
            func_param_descs[idx] = textwrap.fill(desc,
                                                  width=recommended_width,
                                                  replace_whitespace=False,
                                                  subsequent_indent=11 * ' ')
    func_return = get_func_returns(
        api_call['sample_resp'], '--sample-resp' in options)
    return func_desc + ''.join(func_param_descs) + func_return


def get_func_description(api_call, recommended_width, func_args):
    """Get the function description, including Args names: descriptions."""
    api_call['description'] = remove_html(api_call['description'])
    func_desc = textwrap.fill(api_call['description'],
                              width=recommended_width,
                              subsequent_indent=7 * ' ')

    # params sometimes has a value of None or is not a key at all
    if func_args:
        new_api_primitives = set(func_args).difference(set(API_PRIMITIVES))
        for primitive in new_api_primitives:
            msg = 'WARNING: Untracked API Primitive: `' + primitive + \
                  '`.\nPlease create an issue.'
            API_PRIMITIVES[primitive] = msg
            print(msg)
        func_desc += '\n\n    Args:'
        func_desc += ''.join(['\n        @' + arg + ': ' +
                              API_PRIMITIVES[arg] for arg in func_args])

    return func_desc


def get_func_returns(sample_resp, has_add_resp):
    """Get the function's description return part"""
    # ( is first char of (empty)
    type_dict = {'(': '(None)', '[': '(list)', '{': '(dict)'}
    sample_resp_first_letter = sample_resp[0]
    func_return_type = type_dict[sample_resp_first_letter]
    func_return = '\n\n    Returns: ' + func_return_type
    if has_add_resp:  # Adding the sample response is a configurable option.
        sample_resp = sample_resp.replace('\n', '\n' + 8*' ')
        func_return += '\n' + 8*' ' + 'Sample Resp:\n' + 8*' ' + sample_resp
    else:
        func_return += '\n'

    return func_return


def modify_api_calls(api_json, options):
    """Modify API calls in meaningful ways."""
    api_calls = []

    # Flatten API calls, but still record the section
    for api_type in api_json:
        for api_call in api_json[api_type]:
            api_call['section'] = api_type
            api_calls += [api_call]

    for index, api_call in enumerate(api_calls):
        api_calls[index]['gen_api_name'] = generate_api_call_name(
            api_call['http_method'], api_call['path'])
        is_http_get_or_delete = api_call['http_method'] in ['GET', 'DELETE']

        has_params = 'params' in api_call and api_call['params']
        func_args = get_path_args(api_call['path'], has_params)
        api_calls[index]['gen_func_args'] = ', '.join(func_args)
        func_desc = get_function_parts(api_call, func_args, options)
        api_calls[index]['gen_func_desc'] = func_desc

        if is_http_get_or_delete:
            # If get/delete, then params will be appended to url as ?key=value
            api_calls[index]['gen_formatted_url'] = \
                get_formatted_url(api_call['path'], has_params)
            api_calls[index]['gen_data'] = ''
        else:
            # If put/post, then params will be requests' data={'key': 'value'}
            api_calls[index]['gen_formatted_url'] = \
                get_formatted_url(api_call['path'], False)  # No format params
            api_calls[index]['gen_data'] = api_call['params']

    return api_calls
