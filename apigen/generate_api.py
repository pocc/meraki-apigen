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
    meraki-apigen [-ct] (--key <apikey>) [--language <name>]
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
  -c, --comment-curl    Add the sample curl request to the docstring for each
                        function (bash and ruby only). [Not implemented]
  -t, --make-tests      Create test functions with YOUR data. Good for
                        testing API functions that will immediately work.
                        Only GETs will be sent to retrieve this data.
                        [Not implemented]

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

base_url = 'https://api.meraki.com/api/v0'


def get_meraki_apidocs_json():
    """Get all API calls from the docs."""
    meraki_apidocs = 'https://dashboard.meraki.com/api_docs'
    pagetext = requests.get(meraki_apidocs).text
    lower_split = pagetext.split("window.allApisJson = ")[1]
    all_api_docs_str = lower_split.split(";\n  </script>")[0]
    api_json = json.loads(all_api_docs_str)
    all_api_calls = [api_call for api_type in api_json
                     for api_call in api_json[api_type]]
    return all_api_calls


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


def get_params(api_call, api_path):
    """Get all of the params for a function

    In a path, sometimes [networkId] or [organizationId] is just [id].
    Change [id] to the correct longer form. Then get all as parameters.

    Also get all parameters from api_call['param'] if any exist.
    """
    # Get everything in [brackets]
    params = re.findall(r'[\[{]([A-Za-z_]*)[\]}]', api_path) or []
    # Param text is of the form 'param1, param2, param3' for func call
    # params sometimes is not a key in the JSON
    # params sometimes has a value of None
    if 'params' in api_call and api_call['params']:
        for param in api_call['params']:
            params.append(param['name'])

    for index, param in enumerate(params):
        params[index] = make_snake_case(param)

    return params


def get_formatted_url(api_call_path, params):
    """Format the URL string for use in the end function.

    Get the URL string such that parameters passed in can be sent in the
    request by adding them with string.format() in the end function."""
    # The variables that will end up being in the function
    func_vars = ', '.join(re.findall(r'[\[{]([A-Za-z_]*)[\]}]', api_call_path))
    func_vars = make_snake_case(func_vars)
    temp_path = re.sub(r'[\[{][A-Za-z_]*[\]}]', '{}', api_call_path)

    formatted_path = "'{}'.format({})".format(temp_path, func_vars)
    return formatted_path


def get_dict_str(params):
    """Get a dict for parameters that can be later formatted.

    Ex. Given params ['time', 'speed'], returned dict would be
    {{"time": {}, "speed": {} }} so .format can be used.
    """
    param_list = []
    for param in params:
        param_list += ['"' + param + '": {}']
    return '{{' + ', '.join(param_list) + '}}'


def generate_api_call_name(http_type, api_path):
    """Get the API call name as a unique one is not provided."""
    http_type = http_type
    full_path_name_with_empties = api_path.split('/')
    # Sometimes an API call will end with '/'.
    path_name_words = list(filter(None, full_path_name_with_empties))
    api_name_part = ''
    for idx, word in enumerate(path_name_words):
        # For /organizations/[organization_id]/admins/[id]
        # we get get_admins_by_organizationid_by_id
        if word[0] in ['[', '{'] and idx + 1 < len(path_name_words):
            by_var = word[1:-1]  # strip square brackets
            if word == '[id]':  # Make 'id' more descriptive
                by_var = path_name_words[idx-1] + '_id'
            api_name_part += '_by_' + by_var
    # Last words of the path are usually the target of the API call
    # so put them first.
    api_name_part = get_path_last_words(path_name_words) + api_name_part

    if not api_name_part:
        api_name_part = path_name_words[-1]
    api_call_name = http_type.lower() + '_' + make_snake_case(api_name_part)
    return api_call_name


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
    api_calls = get_meraki_apidocs_json()
    todays_date = datetime.datetime.now().isoformat()
    http_stats = get_http_stats(api_calls)
    language = args['--language']
    if not language:
        language = 'python'
    if language not in ['bash', 'python', 'ruby']:
        raise ValueError(
            "Only valid languages are bash, ruby, and python.\n" + __doc__)
    for index, api_call in enumerate(api_calls):
        api_calls[index]['gen_api_name'] = generate_api_call_name(
            api_call['http_method'], api_call['path'])

        api_path = re.sub(r'/([A-Za-z_]*?)/\[id\]', r'/[\1_id]',
                          api_call['path'])
        params = get_params(api_call, api_path)
        if api_call['http_type'] in ['GET', 'DELETE']:
            # If get/delete, then params will be appended to url as ?key=value
            api_calls[index]['gen_formatted_url'] = \
                get_formatted_url(api_path, api_call['params'])
            api_calls[index]['gen_data'] = ''
        else:
            # If put/post, then params will be sent as a dict {'key': 'value'}
            api_calls[index]['gen_formatted_url'] = \
                get_formatted_url(api_path, '')
            api_calls[index]['gen_data'] = get_dict_str(api_call['params'])

        params = ', '.join(params)  # Comma required after params in call.
        api_calls[index]['gen_params'] = params
        max_docstring_first_line_length = 72 - 10  # recommended 72 - both """
        # todo Add option for comment-curl
        # todo Add option for make-tests
        func_desc = api_call['description']
        if len(func_desc) > max_docstring_first_line_length:
            func_desc = textwrap.wrap(func_desc, 68)  # recommended 72 - indent
            func_desc = '\n    '.join(func_desc)
        api_calls[index]['gen_func_desc'] = func_desc

    preamble = get_preamble(todays_date, len(api_calls), http_stats, language)
    if language == 'python':
        mps.make_python_script(api_key, api_calls, preamble, )
    elif language == 'ruby':
        # raise NotImplementedError
        mrs.make_ruby_script(api_key, api_calls, preamble)
    elif language == 'bash':
        # raise NotImplementedError
        mbs.make_bash_script(api_key, api_calls, preamble)


if __name__ == '__main__':
    main()
