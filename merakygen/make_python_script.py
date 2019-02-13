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
import textwrap
import os

import yapf
import pylint.lint as pylinter
import pylint.reporters.text as textreporter


def make_function(func_name, func_desc, func_args,
                  req_http_type, req_url_format):
    """Generate a python function given the paramaters."""
    params_should_be_in_url = req_http_type in ['GET']
    if func_args:  # If there is more than the function description, +newline
        func_desc += '\n    '
    if 'params' in func_args:
        assert req_http_type != 'DELETE'  # Delete should not have params.
        func_args = func_args.replace('params', 'params=\'\'')
        if params_should_be_in_url:
            func_urlencoded_query = """         
    url_query = '?' + '&'.join([key + '=' + params[key] for key in params])"""
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
                func_name=api_call['gen_name'],
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
        print("## https://github.com/pocc/merakygen/issues     ##")
        print(54*"#")


def make_google_style_docstring(description, args, link, params,
                                return_type, return_string):
    """Generate a function docstring in Google-style.

    Args:
        description (string): One or two sentence description of function
        args (dict): All arguments and their descriptions
        link (str): Link to the API call
        params (dict): Additional options for this function
        return_type (str): Type of object that function returns
        return_string (str): Any additional context to the return value

    Returns:
        Google-stlye docstring
    """
    python_docstring_width = 72

    def my_textwrap(text, indent=4):
        """Wrap text with specific settings."""
        text_lines = text.splitlines()
        wrapped_lines = []
        for line in text_lines:
            wrapped_lines += textwrap.wrap(line,
                                           width=python_docstring_width,
                                           expand_tabs=True,
                                           tabsize=4,
                                           replace_whitespace=False,
                                           subsequent_indent=indent*' ')
        return '\n'.join(wrapped_lines)

    if description[-1] != '.':
        description += '.'
    description = my_textwrap(description, indent=7)

    func_docstring = description + '\n\n'
    if link:
        func_docstring += 4*' ' + link + '\n'

    args_docstring = '\n\n\tArgs:'
    for arg in args:
        args_docstring += '\n        ' + arg + ' (str): ' + args[arg]
    args_docstring = my_textwrap(args_docstring, indent=11)
    func_docstring += '\n' + args_docstring

    if params:
        for param in params:
            if type(params[param]) == dict:  # Nested params
                param_line = '\t\t\t' + param + ' (list): ' + \
                             params[param]['description']
                func_docstring += '\n' + my_textwrap(param_line, indent=16) + \
                                  '\n' + 16*' ' + '↳ options:'
                for nested_param in params[param]['options']:
                    np_line = '\t\t\t\t\t' + nested_param + ': ' \
                              + params[param]['options'][nested_param]
                    func_docstring += '\n' + my_textwrap(np_line, indent=24)
            else:
                param_line = '\t\t\t' + param + ': ' + params[param]
                func_docstring += '\n' + my_textwrap(param_line, indent=16)

    return_type_str = '\n\t' + 'Returns: ' + return_type
    if return_string:
        indented_return_string = return_string.replace('\n', '\n\t\t')
        return_docstring = return_type_str + '\n\t\t' + 'Example: ' \
            + indented_return_string
    else:
        return_docstring = return_type_str
    if return_type != 'None':
        func_docstring += '\n\n' + my_textwrap(return_docstring, indent=7)

    return func_docstring


class MakePythonModule:
    """Make a folder that contains the python script and supporting files."""
    def __init__(self, module, script_text):
        self.module_name = module
        self.script_text = script_text

        self.make_python_scaffolding()
        self.save_static_files()
        self.save_script()

    def make_python_scaffolding(self):
        """Make the gem directory structure."""
        folders = [self.module_name]
        for folder in folders:
            if not os.path.isdir(folder):
                os.makedirs(folder)

    def save_static_files(self):
        """Save supporting files (todo save files here)"""
        pass

    def save_script(self):
        """Save all files."""
        filename = self.module_name + '/' + self.module_name + '.py'
        with open(filename, 'w') as myfile:
            print('\t- saving ' + self.module_name + '...')
            myfile.write(self.script_text)


def make_python_script(api_key, api_calls, preamble, options):
    """Make python script."""
    output_file = 'meraki_api.py'
    generated_text = """\
# -*- coding: utf-8 -*-
\"\"\"{}\"\"\"
import json\n\nimport requests\n
BASE_URL = 'https://api.meraki.com/api/v0'
HEADERS = {{
    'X-Cisco-Meraki-API-Key': '{}',
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
        sample_resp = ''
        for api_call in api_calls:
            if '--sample-resp' in options:
                sample_resp = api_call['sample_resp']
            api_call_func_desc = make_google_style_docstring(
                api_call['func_desc'],
                api_call['func_args'],
                api_call['func_link'],
                api_call['func_params'],
                api_call['func_return_type'],
                sample_resp)
            generated_text += make_function(
                func_name=api_call['gen_name'],
                func_desc=api_call_func_desc,
                func_args=api_call['gen_func_args'],
                req_http_type=api_call['http_method'],
                req_url_format=api_call['gen_formatted_url']) \
                + whitespace_between_functions
    MakePythonModule('pacg_meraki', generated_text)
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
