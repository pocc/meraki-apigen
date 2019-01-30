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
"""Meraki-APIgen:
    Code generator for the Meraki API

USAGE:
    meraki-apigen (--key <apikey>) [--language <name>]
                  [--classy] [--lint] [--nowrap]
                  [-h | --help] [-v | --version]

DESCRIPTION:
    Convert all of the recently released Meraki v0 API calls into
    Python or Ruby. As new API calls are released all the time, rerun
    this occasionally.

    This is a work in progress and things are expected to break.

OPTIONS:
  --key <apikey>        Your API key. You can find it by going to your profile.
  --language <name>     Create a script in language. Valid options are
                        python, ruby, and bash. Python is the default.
                        For ruby linting, ruby/gem will need to be installed.
  --classy              Use classes instead of a function list.
  --lint                Call Pylint. If not 10.00/10, print error text.
  --nowrap              Do not wrap text to 79 width with yapf.
                        Default is to wrap.
  -h, --help            Print this help message.
  -v, --version         Print version and exit.

SEE ALSO:
    Contact: Ross Jacobs (rosjacob [AT] cisco.com)
    Github: https://github.com/pocc/meraki-apigen
"""
import json
import sys
import re
import datetime
import collections
import textwrap

import requests
import yapf
import docopt

import apigen
import apigen.make_bash_script as mbs
import apigen.make_python_script as mps
import apigen.make_ruby_script as mrs

BASE_URL = 'https://api.meraki.com/api/v0'
API_PRIMITIVES = {
    'org_id': '(eg 212406)' + '\n' + 12*' ' + '↳ get_orgs()',
    'network_id': '(eg N_24329156)' + '\n' + 12*' ' +
                  '↳ get_networks_by_org_id(org_id)',
    'admin_id': '(eg 212406)' +
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
                       '↳ post_http_servers_webhook_tests_by_network_id('
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
                  '↳ post_profile_clarity_by_network_id(network_id, params)',
    'app_id': 'SM Cisco Polaris app ID (eg 123456)\n' + 12*' ' +
              '↳ get_app_polaris_by_network_id(network_id, params)',
    'sm_id': '???\n' + 12*' ' + '↳ ???',
    'service': 'MX Services (eg \'web\')\n' + 12*' ' +
               '↳ get_firewalled_services_by_network_id(network_id)',
    'vlan_id': 'VLAN number (eg 1234)' +
               '\n' + 12*' ' + '↳ get_vlans_by_network_id(network_id)',
    'switch_port_number': 'like (1-48)\n' + 12*' ' +
                          '↳ get_switch_ports_by_serial(serial)',
}


def get_meraki_apidocs_json():
    """Get all API calls from the docs."""
    meraki_apidocs = 'https://dashboard.meraki.com/api_docs'
    pagetext = requests.get(meraki_apidocs).text
    lower_split = pagetext.split("window.allApisJson = ")[1]
    all_api_docs_str = lower_split.split(";\n  </script>")[0]
    api_json = json.loads(all_api_docs_str)
    return api_json


def get_http_stats(api_calls):
    """Per the API calls, get the number of each http type (GET, POST, ...)"""
    http_types_list = [api_call['http_method'] for api_call in api_calls]
    http_types_counts = dict(collections.Counter(http_types_list))
    return re.sub(r'[\']', '', str(http_types_counts))


def get_preamble(todays_date, num_api_calls, http_stats, lang):
    """Generate the docstring header at the top of the file."""
    header = """Generated and linted at {}
Pulled via the Meraki API v0 (https://dashboard.meraki.com/api_docs/)
API calls: {} {}

Meraki API Generator v{}
    Convert all the recently released API calls into [{}] function calls.
    As new API calls are released all the time, rerun this occasionally.

More Info
    Contact: Ross Jacobs (rosjacob [AT] cisco.com)
    Github: https://github.com/pocc/meraki-apigen
    Issues: https://github.com/pocc/meraki-apigen/issues
""".format(todays_date, num_api_calls, http_stats, apigen.__version__, lang)
    return header


def make_snake_case(input_string):
    """Make a CamelCase string snake_case."""
    temp_string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp_string).lower()


def get_path_args(api_path, has_params):
    """Get all of the arguments for a function

    In a path, sometimes [networkId] or [organizationId] is just [id].
    Change [id] to the correct longer form. Then get all as parameters.
    """
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
        args[index] = make_snake_case(arg)

    if has_params:
        args += ['params']

    return args


def get_formatted_url(api_call_path, has_params):
    """Format the URL string for use in the end function.

    Get the URL string such that parameters passed in can be sent in the
    request by adding them with string.format() in the end function."""
    # The variables that will end up being in the function
    func_vars = ', '.join(get_path_args(api_call_path, has_params))
    func_vars = make_snake_case(func_vars)
    temp_path = re.sub(r'[\[{][A-Za-z_]*[\]}]', '{}', api_call_path)

    formatted_path = "'{}'.format({})".format(temp_path, func_vars)
    return formatted_path


def generate_api_call_name(http_type, api_path):
    """Get the API call name as a unique one is not provided."""
    http_type = http_type
    full_path_name_with_empties = api_path.split('/')
    # Sometimes an API call will end with '/'.
    path_name_words = list(filter(None, full_path_name_with_empties))
    api_name_part = ''
    for idx, word in enumerate(path_name_words):
        # For /organizations/[organization_id]/admins/[id]
        # we get get_admin_id_by_org_id
        if word[0] in ['[', '{'] and idx + 1 < len(path_name_words):
            by_var = word[1:-1]  # strip square brackets
            if word == '[id]':  # Make 'id' more descriptive
                by_var = path_name_words[idx-1] + '_id'
            if word == '[number]':
                by_var = path_name_words[idx-1] + '_number'
            api_name_part += '_by_' + by_var
    # Last words of the path are usually the target of the API call
    # so put them first.
    api_call_name = get_path_last_words(path_name_words) + api_name_part
    api_call_name = api_call_name.replace('organization', 'org')  # Simplify

    if not api_call_name:
        api_call_name = path_name_words[-1]
    api_call_name = http_type.lower() + '_' + make_snake_case(api_call_name)
    return api_call_name


def remove_html(target_string):
    """Remove HTML tags from a string."""
    target_string = re.sub(r'<a[\s\S]*?href=[\'\"]', '', target_string)
    return re.sub(r'[\'\"][\s\S]*?a>', '', target_string)


def get_path_last_words(path_name_words):
    """Get the last words of an API path."""
    # If /**/admins/[id], return 'admins_id'
    if len(path_name_words) > 1 and path_name_words[-1][0] in ['[', '{']:
        return path_name_words[-2] + '_' + path_name_words[-1][1:-1]
    # If /**/[organization_id]/admins or /admins, return 'admins'
    if len(path_name_words) == 1 or path_name_words[-2][0] in ['[', '{']:
        return path_name_words[-1]
    # If /**/clients/latencyStats, return 'clients_latencyStats'
    # so as to differentiate this function from similar ones.
    return path_name_words[-2] + '_' + path_name_words[-1]


def get_function_parts(api_call, func_args, is_classy):
    """Get the function description and arguments and return as a tuple."""
    class_indent = bool(not is_classy) * 4  # Classes need indent
    recommended_width = 68 + class_indent
    api_call['description'] = remove_html(api_call['description'])
    func_desc = textwrap.fill(api_call['description'],
                              width=recommended_width,
                              subsequent_indent=7 * ' ')
    func_param_descs = []
    # params sometimes has a value of None or is not a key at all
    if func_args:
        new_api_primitives = set(func_args).difference(set(API_PRIMITIVES))
        for primitive in new_api_primitives:
            API_PRIMITIVES[primitive] = \
                "Untracked API Primitive. Please create an issue."
        func_desc += '\n\n    args:'
        func_desc += ''.join(['\n        @' + arg + ': ' +
                              API_PRIMITIVES[arg] for arg in func_args])
    params = {}
    if 'params' in api_call and api_call['params']:
        func_desc += '\n\n    params (dict):'
        params = api_call['params']
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
    total_func_desc = func_desc + ''.join(func_param_descs)
    return total_func_desc, params


def modify_api_calls(args, api_json):
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

        api_path = re.sub(r'/([A-Za-z_]*?)/\[id\]', r'/[\1_id]',
                          api_call['path'])
        has_params = 'params' in api_call and api_call['params']
        func_args = get_path_args(api_path, has_params)
        api_calls[index]['gen_func_args'] = ', '.join(func_args)
        func_desc, params =\
            get_function_parts(api_call, func_args, args['--classy'])
        api_calls[index]['gen_func_desc'] = func_desc

        if api_call['http_method'] in ['GET', 'DELETE']:
            # If get/delete, then params will be appended to url as ?key=value
            api_calls[index]['gen_formatted_url'] = \
                get_formatted_url(api_path, has_params)
            api_calls[index]['gen_data'] = ''
        else:
            # If put/post, then params will be requests' data={'key': 'value'}
            api_calls[index]['gen_formatted_url'] = \
                get_formatted_url(api_path, has_params)
            api_calls[index]['gen_data'] = params

    return api_calls


def main():
    """Main func.
    Should take care of all functions that are shared across languages."""
    args = docopt.docopt(__doc__)
    if args['--version']:
        python_ver = sys.version.replace('\n', '')
        print('Meraki-APIgen', apigen.__version__, '\n\nPython', python_ver)
        print('\trequests', requests.__version__, '\n\tyapf', yapf.__version__)
        print('Testing/linting')
        ruby_ver, gem_ver = mrs.get_ruby_versions()
        print('\truby', ruby_ver, '\n\tgem', gem_ver)
        print('\tbash', mbs.get_bash_version())
        sys.exit()
    # Python is default
    api_key = args['--key']
    api_json = get_meraki_apidocs_json()

    api_calls = modify_api_calls(args, api_json)

    todays_date = datetime.datetime.now().isoformat()
    http_stats = get_http_stats(api_calls)
    language = args['--language']
    if not language:
        language = 'python'
    if language not in ['bash', 'python', 'ruby']:
        raise ValueError(
            "Only valid languages are bash, ruby, and python.\n" + __doc__)
    preamble = get_preamble(todays_date, len(api_calls), http_stats, language)
    # Reformatting args so that other modules can use options like a dict
    args['textwrap'] = not args['--nowrap']
    options = [arg.replace('--', '') for arg in args if args[arg]]
    if language == 'python':
        mps.make_python_script(api_key, api_calls, preamble, options)
    elif language == 'ruby':
        mrs.make_ruby_script(api_key, api_calls, preamble, options)
        raise NotImplementedError
    elif language == 'bash':
        mbs.make_bash_script(api_key, api_calls, preamble)
        raise NotImplementedError


if __name__ == '__main__':
    main()