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
"""Generate a powershell module."""
import re
import os
import subprocess as sp
import shutil

import merakygen


def make_function(func_name, func_desc, func_args,
                  req_http_type, req_url_format):
    """Generate a powershell function given the paramaters."""
    params_should_be_in_url = req_http_type in ['GET', 'DELETE']
    if func_args:  # If there is more than the function description, +newline
        func_desc += '\n    '
        # Preface all func args with $
        func_args = '$' + func_args.replace(', ', ', $')
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
    function_text = """function {0}({1}) {{
    <#{2}#>{3}
    response = requests.{4}(BASE_URL + {5},{6} headers=HEADERS)
    return graceful_exit(response)
}}""".format(
        func_name,
        func_args,
        func_desc,
        func_urlencoded_query,
        req_http_type.lower(),
        req_url_format,
        req_data
    )
    return function_text


def make_classes(api_calls):
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


class MakePSModule:
    """Make a powershell module.

    Structure taken from https://github.com/pcgeek86/PSGitHub
    """
    def __init__(self, module):
        self.module = module
        self.make_folders()
        self.copy_entrypoint()
        self.make_module_manifest()

    def make_folders(self):
        """Make folders for Powershell module structure.
        /MerakiAPI
            /Classes :  Classes that contain schemas for objects
                        like org, network, admin
            /Functions
                /Private : Where functions that are required by
                           generated functions go.
                /Public : Where generated functions go
            MerakiAPI.psd1 : Required module metadata file
            MerakiAPI.psm1 : Required module entry point
        """
        folders = [
            self.module + '/Classes',
            self.module + '/Functions/Private',
            self.module + '/Functions/Public'
        ]
        for folder in folders:
            if not os.path.isdir(folder):
                os.makedirs(folder)

    def copy_entrypoint(self):
        """Copy the required entrypoint .psm1 file to the module."""
        shutil.copy('assets/MerakiAPI.psm1', self.module)

    @staticmethod
    def find_ps_functions(file):
        """Find all powershell functions in a file and return the list."""
        with open(file) as ps_file:
            ps_filetext = ps_file.read()
        functions = re.findall(r'function ([A-Za-z-_]+)', ps_filetext)
        return functions

    @staticmethod
    def convert_py_list_to_ps_list(python_list):
        """Convert a python list (str) to a powershell list (str)."""
        return '@(' + str(python_list)[1:-1] + ')'

    def make_module_manifest(self):
        """Generate the psd1 file required for PS packages."""
        base_filename = os.getcwd() + '/' + self.module + '/'
        ps_function_list = self.find_ps_functions('meraki_api.ps1')
        ps_function_str = self.convert_py_list_to_ps_list(ps_function_list)
        # Cannot supply entire changelog as max for -ReleaseNotes is 840 chars.
        most_recent_release_notes = merakygen.__changelog__.split('\n\n')[0]
        license_path = '/blob/master/LICENSE.txt'
        powershell_cmd = 'pwsh'
        cmd_list = [
            powershell_cmd, '-Command', 'New-ModuleManifest',
            '-Path', base_filename + self.module + '.psd1',
            '-PowerShellVersion', '5.0',
            '-Author', 'Ross Jacobs' + ' <rossbjacobs@gmail.com>',
            '-CompanyName', 'Ross Jacobs',
            '-Copyright', 'Ross Jacobs 2019 All Rights Reserved.',
            '-ModuleVersion', merakygen.__version__,
            '-Description', merakygen.__description__,
            '-Tags', '@("Meraki", "API", "Networking")',
            '-HelpInfoUri', merakygen.__project_url__,
            '-ProjectUri', merakygen.__project_url__,
            '-LicenseUri', merakygen.__project_url__ + license_path,
            '-ReleaseNotes', most_recent_release_notes,
            '-FunctionsToExport', ps_function_str,
            '-RootModule', base_filename + self.module + '.psm1',
        ]
        # Sanitize after assigning for readability.
        for index, cmd in enumerate(cmd_list):
            cmd_list[index] = ps_sanitize(cmd)
        sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
        sp_outputs = sp_pipe.communicate()
        if sp_outputs[0] or sp_outputs[1]:
            print("PS MODULE STDOUT: " + sp_outputs[0].decode('utf-8') +
                  "PS MODULE STDERR: " + sp_outputs[1].decode('utf-8'))


def ps_sanitize(text):
    """Add powershell escape chars to strings sent to powershell"""
    text = re.sub(r'([ $#`<>])', '`\\1', text)
    return text.replace('\n', '`n').replace('\t', '`t')


def make_powershell_script(api_key, api_calls, preamble, options):
    """Make powershell script."""
    module_name = 'MerakiAPI'
    MakePSModule(module=module_name)

    public_func_dir = os.getcwd() + '/' + module_name + '/Functions/Public'
    for api_call in api_calls:
        generated_text = make_function(
            func_name=api_call['gen_name'],
            func_desc=api_call['gen_func_desc'],
            func_args=api_call['gen_func_args'],
            req_http_type=api_call['http_method'],
            req_url_format=api_call['gen_formatted_url']) \
            + '\n'
        func_file_path = public_func_dir + '/' + api_call['gen_name'] + '.ps1'
        with open(func_file_path, 'w') as myfile:
            print('\t- saving ' + api_call['gen_name'] + '.ps1' + ' ...')
            myfile.write(generated_text)

    print("\npowershell module generated!")
