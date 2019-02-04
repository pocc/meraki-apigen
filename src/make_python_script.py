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
"""Generate python script."""
import re

import yapf
import pylint.lint as pylinter
import pylint.reporters.text as textreporter


def make_function(func_name, func_desc, func_args,
                  req_http_type, req_url_format):
    """Generate a python function given the paramaters."""
    params_should_be_in_url = req_http_type in ['GET', 'DELETE']
    if func_args:  # If there is more than the function description, +newline
        func_desc += '\n    '
    if 'params' in func_args:
        func_args = func_args.replace('params', 'params=\'\'')
        if params_should_be_in_url:
            func_urlencoded_query = """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')"""
            # Add additional format variable for params arg to be sent in
            req_url_format = req_url_format.replace("\'.format", "{}\'.format")
            assert req_url_format.count(')') <= 1  # Should only be format's )
            req_url_format = req_url_format.replace(')', ', url_query)')
            req_data = ''
        else:  # req_http_type in ['PUT', 'POST'], data in requests body
            func_urlencoded_query = ''
            req_data = 'data=json.dumps(params), '
    else:
        func_urlencoded_query = ''
        req_data = ''
    function_text = """\ndef {0}({1}):
    \"\"\"{2}\"\"\"{3}
    response = requests.{4}(BASE_URL + {5},{6} headers=HEADERS)
    return graceful_exit(response)""".format(
        func_name,
        func_args,
        func_desc,
        func_urlencoded_query,
        req_http_type.lower(),
        req_url_format,
        req_data
    )
    return function_text


def make_classy(api_calls):
    """Add class headers and indent all functions once.

    Go through API calls and group them by section. Then add the sections
    together into a string.
    """
    api_sections = {}
    generated_text = ''
    for api_call in api_calls:
        section_name = api_call['section'].title().replace(' ', '')
        if section_name not in api_sections:
            api_sections[section_name] = []
        api_sections[section_name].append(api_call)

    whitespace_between_methods = '\n'
    for section in api_sections:
        generated_text += """\
\n\nclass {0}:
    \"\"\"Class to access {0} functions.\"\"\"""".format(section)

        for api_call in api_sections[section]:
            function_text = '\n@staticmethod' + make_function(
                func_name=api_call['gen_api_name'],
                func_desc=api_call['gen_func_desc'],
                func_args=api_call['gen_func_args'],
                req_http_type=api_call['http_method'],
                req_url_format=api_call['gen_formatted_url'])
            function_text += whitespace_between_methods
            # Class methods are indented one more than functions.
            indent_regex = r'\n([ ]*?[\S]+?)'  # Only indent text, not \n
            generated_text += re.sub(indent_regex, r'\n    \1', function_text)

    return generated_text


def lint_output(file):
    """Apply pylint to code text."""
    class WritableObject:
        # pylint: disable=too-few-public-methods
        """Quick class to accept pylint output and write it to string."""
        def __init__(self):
            self.text = ''

        def write(self, pylint_line):
            """Append pylint output to list."""
            self.text += pylint_line

    pylint_output = WritableObject()
    # Disable large file error (by design), and too few/many public methods
    # Some classes will have 1 function and SM has 37.
    pylinter.Run(args=[file, '--disable=C0302,R0903,R0904'],
                 reporter=textreporter.TextReporter(pylint_output),
                 do_exit=False)
    if pylint_output.text and 'rated at 10.00/10' not in pylint_output.text:
        print(pylint_output.text + 54 * '#')
        print("## Pylint check is FAILING. Please submit an issue! ##")
        print("## https://github.com/pocc/meraki-apigen/issues     ##")
        print(54*"#")


def make_python_script(api_key, api_calls, preamble, options):
    """Make python script."""
    output_file = 'meraki_api.py'
    generated_text = """\
# -*- coding: utf-8 -*-
\"\"\"{}\"\"\"
import json\nimport urllib.parse\n\nimport requests\n
BASE_URL = 'https://api.meraki.com/api/v0'
HEADERS = {{
    'X-Cisco-Meraki-API-Key': {},
    'Content-Type': 'application/json'
}}


def graceful_exit(response):
    \"\"\"Gracefully exit from the function.
    
    JSON:
        200: Successful GET, UPDATE
        201: Successful POST
    
    {{}}:
        204: Successful DELETE
        400: Bad request. Correct/check your params
        404: Resource not found. Correct/check your params
        500: Server error
    
    Args:
        response (Requests): The requests object from the function call.
    Returns:
        JSON if one is available. Return status code (int) if not.
    \"\"\"
    try:
        resp_json = json.loads(response.text)
        if 'errors' in resp_json:
            raise ConnectionError(resp_json['errors'])
        if type(resp_json) == json:
            resp_json['status_code'] = response.status_code
        return resp_json
    except ValueError:
        return response.status_code
""".format(preamble, api_key)
    if 'classy' in options:
        generated_text += make_classy(api_calls)
    else:
        whitespace_between_functions = '\n\n'
        for api_call in api_calls:
            generated_text += make_function(
                func_name=api_call['gen_api_name'],
                func_desc=api_call['gen_func_desc'],
                func_args=api_call['gen_func_args'],
                req_http_type=api_call['http_method'],
                req_url_format=api_call['gen_formatted_url']) \
                + whitespace_between_functions
    with open(output_file, 'w') as myfile:
        print('\t- saving ' + output_file + '...')
        myfile.write(generated_text)
    if '--textwrap' in options:
        print('\t- text wrapping ' + output_file + '...')
        yapf.yapf_api.FormatFile(
            filename=output_file,
            in_place=True,
            style_config='pep8',
            verify=True)
    if '--lint' in options:
        print('\t- linting ' + output_file + '...')
        lint_output(output_file)
    print("\nPython module generated!")
