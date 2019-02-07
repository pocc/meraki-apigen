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
"""Generate the function docstring given a function."""
import re


APIDOCS_BASE_URL = 'https://dashboard.meraki.com/api_docs'
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


def get_function_docstring(api_call, func_args):
    """Get the function docstring."""
    api_call['func_desc'] = get_func_description(api_call['description'])
    api_call['func_args'] = get_func_args(func_args)
    api_call['func_link'] = get_api_link(api_call)
    api_call['func_params'] = get_function_params(api_call)
    api_call['func_return_type'] = get_func_type(api_call['sample_resp'])
    return api_call


def get_func_description(api_call_description):
    """Get the function description, including Args names: descriptions."""
    return remove_html(api_call_description)


def get_func_args(func_args):
    """Get the function args."""
    func_args_with_descs = {}
    # params sometimes has a value of None or is not a key at all
    if func_args:
        new_api_primitives = set(func_args).difference(set(API_PRIMITIVES))
        for primitive in new_api_primitives:
            msg = 'WARNING: Untracked API Primitive: `' + primitive + \
                  '`.\nPlease create an issue.'
            API_PRIMITIVES[primitive] = msg
            print(msg)
        for arg in func_args:
            func_args_with_descs[arg] = API_PRIMITIVES[arg]

    return func_args_with_descs


def get_function_params(api_call):
    """Get the function parameters from the API call."""
    has_params = 'params' in api_call and api_call['params']
    func_params = {}
    if has_params:
        for index, param in enumerate(api_call['params']):
            param_description = remove_html(param['description'])
            has_nested_params = 'params' in param
            if has_nested_params:
                func_params[param['name']] = {
                    'description': param_description
                }

                for nested_param in param['params']:
                    func_params[param['name']][nested_param['name']] = \
                        nested_param['description']
                    # Params should not be nested more than 2 deep.
                    if 'is_array' in nested_param:
                        assert(not nested_param['is_array'])
                    assert('params' not in nested_param)
            else:
                func_params[param['name']] = param_description

    return func_params


def get_api_link(api_call):
    """Get the API link from description."""
    desc_first_sentence = api_call['description'].split('.')[0]
    link_words = re.sub(r'[\'\(\)\-,]', '', desc_first_sentence)
    link_words = re.sub(r'[ ]+', ' ', link_words)  # Remove redundant spaces
    hypenated_link_words = re.sub(r'[ \/]', '-', link_words.lower())
    return APIDOCS_BASE_URL + '#' + hypenated_link_words


def get_func_type(sample_resp):
    """Get the function's description return part"""
    # ( is first char of (empty)
    type_dict = {'(': 'None', '[': 'list', '{': 'dict'}
    sample_resp_first_letter = sample_resp[0]
    return type_dict[sample_resp_first_letter]


def remove_html(target_string):
    """Remove HTML tags from a string."""
    target_string = re.sub(r'<a[\s\S]*?href=[\'\"]', '', target_string)
    return re.sub(r'[\'\"][\s\S]*?a>', '', target_string)
