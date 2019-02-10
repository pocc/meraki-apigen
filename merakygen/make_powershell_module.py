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
import textwrap

import inflection as inf

import merakygen


def make_function(func_name, func_desc, func_args_descs,
                  req_http_type, url_path):
    """Generate a powershell function given the paramaters."""
    if func_args_descs:
        # Add $ to variables and convert to camelCase
        func_params = 'param('
        func_param_list = []
        for index, arg in enumerate(func_args_descs):
            param_options = 'Position={}'.format(index)
            if 'params' not in arg:
                param_options += ', Mandatory=$True'
            param_options += ', HelpMessage=' + func_args_descs[arg]
            func_param_list += ['\n[parameter({})]'.format(param_options) +
                                '\n[String]$' + inf.camelize(arg, False)]
        func_params += ','.join(func_param_list)
        # $params are found in function call, not in format replacement
        url_path = url_path.replace(', $params', '')
        # Replace [args] in url path with the camelCase variable names.
        regex = r'[\[\{][A-Za-z-_]*[\]\}]'
        for idx, match in enumerate(re.findall(regex, url_path)):
            index_arg = '$' + inf.camelize(list(func_args_descs)[idx], False)
            url_path = url_path.replace(match, index_arg)
        func_params += '\n)'
    else:
        func_params = 'param()'
    params_should_be_in_url = req_http_type == 'GET'
    if 'params' in list(func_args_descs):
        assert req_http_type != 'DELETE'  # Delete should not have URL params.
        func_params = func_params.replace('params', 'params=\'\'')
        if params_should_be_in_url:
            func_urlencoded_query = """$urlParams = ParseParams($params)"""
            url_path += '$urlParams'
            req_data = '\'\''
        else:  # req_http_type in ['PUT', 'POST'], data in requests body
            func_urlencoded_query = ''
            req_data = '$params'
    else:
        func_urlencoded_query = ''
        req_data = '\'\''
    url_path = "\"" + url_path + "\""
    function_text = """\
function {0} {{
<#
{1}
#>
[cmdletbinding()]
{2}
    {3}
    return Invoke-ApiCall "{5}" {4} {6}
}}""".format(
        func_name,
        func_desc,
        func_params,
        func_urlencoded_query,
        url_path,
        req_http_type.lower(),
        req_data
    )
    return function_text


def make_function_comment(preamble, description, args, link, params,
                          return_type, call_path, return_string):
    """Based on

    https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comment_based_help?view=powershell-6
    Generate Powershell comments-based help. Each item will start with a '.',
    be all caps, and have a newline following its section.

        Example:
            <#
            .SYNOPSIS
                Create an admin.

            .PARAMETER
                ...
            #>

    Args:
        preamble (str): An "about this program" added to every function.
        description (string): One or two sentence description of function
        args (dict): All arguments and their descriptions
        link (str): Link to the API call
        params (dict): Additional options for this function
        return_type (str): Type of object that function returns
        call_path (str): /path/to/endpoint/url, ('path' key in orig json)
        return_string (str): Any additional context to the return value

    Returns:
        Powershell-stlye function comment
    """
    # Powershell code should wrap at 120, but Get-Help wraps comments at 84.
    powershell_docstring_width = 84
    # Translate all variable names into camelCase
    local_args = dict(args)
    for arg in list(local_args):
        local_args[inf.camelize(arg, False)] = local_args[arg]
        local_args.pop(arg)

    def my_textwrap(text, indent=0):
        """Wrap text with specific settings."""
        text_lines = text.splitlines()
        wrapped_lines = []
        for line in text_lines:
            wrapped_lines += textwrap.wrap(line,
                                           width=powershell_docstring_width,
                                           expand_tabs=True,
                                           tabsize=4,
                                           replace_whitespace=False,
                                           subsequent_indent=indent*' ')
        return '\n'.join(wrapped_lines)

    comment_sections = []
    if description[-1] != '.':
        description += '.'
    synopsis = '.SYNOPSIS' + '\n' + my_textwrap(description)
    comment_sections += [synopsis]

    comment_sections += ['.DESCRIPTION\n' + preamble]

    if link:
        comment_sections += ['.LINK\n' + link]

    args_docstring = ''
    for arg in local_args:
        args_docstring += '.PARAMETER ' + arg + '\n ' + local_args[arg]
    args_docstring = my_textwrap(args_docstring)
    comment_sections += [args_docstring]

    if params:
        parameter_docstring = '.PARAMETER params\nJSON string ' \
                              'like \'{"key":"value", ...}\''
        for param in params:
            if type(params[param]) == dict:  # Nested params
                # Remove the s from param (if it has nested, it WILL have an s)
                param_element = param[:-1]
                parameter_docstring += '\n\nKEY "' + param + '": ' + \
                    params[param]['description'] + '\n    [$' + \
                    param_element + ', ...], $' + param_element + ' = {'
                np_line_list = []
                for nested_param in params[param]['options']:
                    nested_description = params[param]['options'][nested_param]
                    np_line_list.append('\t\t"' + nested_param + '": $(' +
                                        nested_description + ')')
                np_lines = ',\n'.join(np_line_list)
                parameter_docstring += '\n' + my_textwrap(np_lines, indent=12)
                parameter_docstring += '\n    ' + '}'
            else:
                param_ln = 'KEY "' + param + '": ' + params[param]
                parameter_docstring += '\n\n' + my_textwrap(param_ln, indent=4)

        # my_textwrap should have taken all tabs out of parameter_docstring
        assert('\t' not in parameter_docstring)
        comment_sections += [parameter_docstring]

    comment_sections += ['.NOTES\nOriginal endpoint path =' + call_path]

    convert_to_ps_types = {
        'None': '',
        'list': 'System.Collections.Arraylist',
        'dict': 'System.Collections.Hashtable',
    }
    return_type_str = '.OUTPUTS\nSystem.String. Can be converted to' + \
                      ' [' + convert_to_ps_types[return_type] + ']'
    output_str = my_textwrap(return_type_str)
    if return_string:
        return_string = '  \'' + return_string.replace('\n', '\n  ')
        output_str += '\n\nSample Response:\n' + return_string + '\''
    comment_sections += [output_str]

    func_docstring = '\n\n'.join(comment_sections)
    # Change indent for lines with ↳ to 4 spaces.
    func_docstring = re.sub(r'\n[\s]*↳', '\n     ↳', func_docstring)
    # Indent comments (.VAR -> 1\t, var's description -> 2\t)
    func_docstring = re.sub(r'\n([ ]*[^\.\n])', '\n    \\1', func_docstring)

    return func_docstring


def get_func_inputs():
    """Generate the function inputs."""
    return 'pass'


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
                url_path=api_call['gen_formatted_url'])
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
        self.copy_private_functions()
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
        shutil.copy('../static/powershell/MerakiAPI.psm1', self.module)

    def copy_private_functions(self):
        """Copy shared private functions that generated functions use."""
        files = os.listdir('../static/powershell/Private')
        for file in files:
            file = os.path.abspath('../static/powershell/Private/' + file)
            shutil.copy(file, self.module + '/Functions/Private')

    def find_ps_functions(self):
        """Find all powershell functions in folder and return the list."""
        ps_files = os.listdir(self.module + '/Functions/Public')
        return [ps_file.replace('.ps1', '') for ps_file in ps_files]

    @staticmethod
    def convert_py_list_to_ps_list(python_list):
        """Convert a python list (str) to a powershell list (str)."""
        return '@(' + str(python_list)[1:-1] + ')'

    def make_module_manifest(self):
        """Generate the psd1 file required for PS packages."""
        base_filename = os.getcwd() + '/' + self.module + '/'
        ps_function_list = self.find_ps_functions()
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


def truncate_func_name(api_calls):
    """Remove Verb-NounByNoun if it would not cause name collisions.

    Unlike programming languages like python/ruby, the extra context
    may not be helpful in usage.

    If removing ByNoun... would produce a collision, keep all function names
    that would produce that collision.
    """
    api_calls_sans_by = [re.sub(r'By.*$', '', api_call['gen_name'])
                         for api_call in api_calls]
    for api_call in api_calls:
        truncated_name = re.sub(r'By.*$', '', api_call['gen_name'])
        name_collision_exists = api_calls_sans_by.count(truncated_name) > 1
        if not name_collision_exists:
            api_call['gen_name'] = truncated_name

    return api_calls


def make_powershell_script(api_key, api_calls, preamble, options):
    """Make powershell script."""
    module_name = 'MerakiAPI'
    MakePSModule(module=module_name)

    public_func_dir = os.getcwd() + '/' + module_name + '/Functions/Public'
    sample_resp = ''
    for api_call in api_calls:
        if '--sample-resp' in options:
            sample_resp = api_call['sample_resp']
        api_call_function_comment = make_function_comment(
            preamble,
            api_call['func_desc'],
            api_call['func_args'],
            api_call['func_link'],
            api_call['func_params'],
            api_call['func_return_type'],
            api_call['path'],
            sample_resp)
        generated_text = make_function(
            func_name=api_call['gen_name'],
            func_desc=api_call_function_comment,
            func_args_descs=api_call['func_args'],
            req_http_type=api_call['http_method'],
            url_path=api_call['path']) \
            + '\n'
        func_file_path = public_func_dir + '/' + api_call['gen_name'] + '.ps1'
        with open(func_file_path, 'w') as myfile:
            print('\t- saving ' + api_call['gen_name'] + '.ps1' + ' ...')
            myfile.write(generated_text)

    print("\nPowershell module generated!")
