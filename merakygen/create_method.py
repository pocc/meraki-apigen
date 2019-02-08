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

import inflection as inf

from merakygen import __version__ as apigen_version
import merakygen.create_function_docstring as docs

API_BASE_URL = 'https://api.meraki.com/api/v0'


def get_http_stats(api_calls):
    """Per the API calls, get the number of each http type (GET, POST, ...)"""
    http_types_list = [api_call['http_method'] for api_call in api_calls]
    http_types_counts = dict(collections.Counter(http_types_list))
    return re.sub(r'[\']', '', str(http_types_counts))


def get_preamble(cli_options, num_api_calls, http_stats, lang):
    """Generate the docstring header at the top of the file."""
    cli_options.insert(0, lang)
    date = datetime.datetime.now().isoformat()
    options_str = ' '.join(cli_options)
    header = """Generated @ {}
Command: `merakygen --key <key> --language {}`

Meraki API Generator v{}
    Convert all Meraki API calls into [{}] function calls.
    As new API calls are released all the time, rerun this occasionally.
    Pulled data from Meraki API v0 (https://dashboard.meraki.com/api_docs/)
    API calls: {} {}

More Info
    Author: Ross Jacobs (rosjacob [AT] cisco.com)
    Github: https://github.com/pocc/meraki-merakygen
    Issues: https://github.com/pocc/meraki-merakygen/issues\
""".format(date, options_str,  apigen_version, lang, num_api_calls, http_stats)
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


def generate_api_call_words(http_type, api_path):
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
                words = [word_before, word]
            else:
                words = [word]
            if i == 0:
                if is_get:
                    word_before = inf.pluralize(word_before)
                return [http_type] + [word_before] + ['by'] + words
            if i > 0:
                if not is_get and 'settings' not in word_list[-1]:
                    word_list[-1] = inf.singularize(word_list[-1])
                return [http_type] + word_list + ['by'] + words
        word_list.insert(0, word)

    return [http_type] + word_list  # For GET /organizations with no [args]


def generate_func_name(api_call, language):
    """Convert the api call words to a function name, per language."""
    api_call_words = generate_api_call_words(
        api_call['http_method'], api_call['path'])
    # default is snake_case for ruby and python
    if language in ['python', 'ruby']:
        api_call_name = '_'.join(api_call_words)
    elif language in ['go', 'javascript']:  # CamelCase
        title_words = ''.join([word.title() for word in api_call_words])
        api_call_name = title_words.title().replace('_', '')
    else:  # powershell with Semi-CamelCase (Verb-NounNoun...)
        # https://docs.microsoft.com/en-us/powershell/developer/cmdlet/approved-verbs-for-windows-powershell-commands
        convert_to_approved_verb = {
            'GET': 'Get', 'POST': 'Add', 'PUT': 'Set', 'DELETE': 'Remove'}
        approved_verb = convert_to_approved_verb[api_call['http_method']]
        nouns = ''.join([word.title() for word in api_call_words[1:]])
        no_underscore_nouns = nouns.replace('_', '')
        api_call_name = approved_verb + '-' + no_underscore_nouns

    return api_call_name


def modify_api_calls(api_json, options, language):
    """Modify API calls in meaningful ways."""
    api_calls = []

    # Flatten API calls, but still record the section
    for api_type in api_json:
        for api_call in api_json[api_type]:
            api_call['section'] = api_type
            api_calls += [api_call]

    for index, api_call in enumerate(api_calls):
        api_calls[index]['gen_name'] = generate_func_name(api_call, language)

        has_params = 'params' in api_call and api_call['params']
        func_args = get_path_args(api_call['path'], has_params)
        api_calls[index]['gen_func_args'] = ', '.join(func_args)
        api_calls[index] = docs.get_function_docstring(api_call, func_args)

        is_post_or_put = api_call['http_method'] in ['POST', 'PUT']
        # If put/post, then params will be requests' data={'key': 'value'}
        # If get, then params will be appended to url as ?key=value&key=value..
        if 'params' in api_call:
            api_calls[index]['gen_data'] = api_call['params']
        else:
            api_calls[index]['gen_data'] = ''
        api_calls[index]['gen_formatted_url'] = get_formatted_url(
            api_call['path'], has_params and is_post_or_put)

    return api_calls
