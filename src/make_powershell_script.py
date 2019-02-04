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
"""Generate a powershell module.

Structure taken from https://github.com/pcgeek86/PSGitHub
"""
import re
import os
import subprocess as sp

from . import __version__


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
    function_text = """\nfunction {0}({1}):
    <#{2}#>{3}
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


class MakePSModule:
    """Make a powershell module."""
    def __init__(self, module):
        self.module = module
        self.make_folders()
        self.make_module_manifest()

    def make_folders(self):
        """Make folders for Powershell module structure.

        /PSMeraki
            /Classes
            /Functions
                /Private
                /Public
            PSMeraki.psd1
            PSMeraki.psm1
        """
        os.makedirs(self.module + '/Classes')
        os.makedirs(self.module + '/Classes/Private')
        os.makedirs(self.module + '/Classes/Public')

    def make_module_manifest(self):
        """Generate the psd1 file required for PS packages."""
        filename = os.getcwd() + '/' + self.module + '.psd1'
        cmd_list = ['Powershell', 'New-ModuleManifest',
                    '-Path', filename,
                    '-PowerShellVersion', '5.0',
                    '-Author', 'Ross Jacobs <rossbjacobs@gmail.com>',
                    '-CompanyName', '',
                    '-Copyright', 'Ross Jacobs 2019 All Rights Reserved.',
                    '-RootModule', 'string',
                    '-ModuleVersion', __version__,
                    '-Description', <string>]

        sp.Popen(


def make_powershell_script(api_key, api_calls, preamble, options):
    """Make powershell script."""
    MakePSModule(module='PSMeraki')
    output_file = 'meraki_api.ps1'
    generated_text = """\
# -*- coding: utf-8 -*-
<#{}#>
class ApiCall
{{
    [string] $apiKey = "{}"
    [hashtable] $headers = @{{ 'X-Cisco-Meraki-API-Key' = $this.apiKey }}

    # Optional method params don't exist so overload functions instead.
    [string] SendRequest([string]$httpMethod, [string]$endpointUrl) {{
        $emptyParams = ''
        return $this.SendRequest($httpMethod, $endpointUrl, $emptyParams)}}
    [string] SendRequest([string]$httpMethod, [string]$endpointUrl, [string]$params) {{
        # Gather/Format API call inputs for Send Request and then call
        # Using Invoke-WebRequest over Invoke-RestMethod because the former has more
        # metadata like StatusCodes.
        $this.utils.print("`nCalling $($httpMethod) on $($endpointUrl) with [$($params)] params.")
        $url = "https://api.meraki.com/api/v0$($endpointUrl)"
        $RespErr = ''

        try {{
            if ($params) {{
                $result = Invoke-WebRequest -Uri $url -Headers $this.headers -Body $params `
                                -method $httpMethod -ContentType 'Application/Json' -ErrorVariable RespErr
            }}
            else
            {{
                $result = Invoke-WebRequest -Uri $url -Headers $this.headers `
                                -method $httpMethod -ContentType 'Application/Json' -ErrorVariable RespErr
            }}
            # Keeping for troubleshooting purposes
            $statusCode = $result.StatusCode

            # Get data and remove trailing whitespace
            $data = $result.Content -replace "[\s]*$",""
            return $data
        }}
        catch {{
            $data = $RespErr
            $statusCode = $_.Exception.Response.StatusCode.Value__
            $this.utils.print("Status code: $($statusCode); Data: $($data)")
            return $data
        }}
    }}
}}


def graceful_exit(response):
    <#Gracefully exit from the function.
    
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
    #>
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
    # Always use classes in powershell
    generated_text += make_classes(api_calls)
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
    print("\npowershell module generated!")
