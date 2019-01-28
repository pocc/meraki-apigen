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
"""Generate bash script."""
import subprocess as sp
import re


def get_bash_version():
    """Get the bash version if it exists and a message if it does not.

    Should return a string like '3.2.57(1)-release (x86_64-apple-darwin18)'
    """
    try:
        cmd_list = ['bash', '--version']
        sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE)
        sp_stdout = sp_pipe.communicate()[0].decode('utf-8')
        version_info = sp_stdout.split('version ')[1].split('\n')[0]
        return version_info
    except FileNotFoundError:
        msg = 'not found (required for bash testing)'
        return msg


def make_bash_function(func_name, func_params, func_desc, sample_req):
    """Should work for HTTP GET"""

    function_text = """

{}
{}() {{
  {}
}}""".format(
        func_desc,
        func_name,
        sample_req
    )
    return function_text


def make_bash_script(api_key, api_calls, preamble):
    """Make bash script."""
    preamble = '#!/bin/bash\n' + preamble
    # Put a '# ' in front of every line except first ^.
    generated_text = preamble.replace('\n', '\n# ')[:-2]
    generated_text += '\nAPIKEY=' + api_key
    generated_text += '\nBASEURL=https://api.meraki.com/api/v0\n'
    for api_call in api_calls:
        sample_req = api_call['sample_req'].replace('<key>', '$APIKEY')
        # Each curl option gets its own line. Don't split if it is already.
        if '\n' not in sample_req:
            sample_req = sample_req.replace(' -', '\\\n    -')
        else:
            sample_req = sample_req.replace('\n  -', '\n    -')
        num_path_params = len(re.findall(r'[\[{]', api_call['path']))
        # Create a list like ['$1', '$2', '$3', '$4', '$5'] for formatting
        var_list = ['${}'.format(i) for i in range(1, num_path_params+1)]
        api_path = '$BASEURL' + re.sub(
            r'[\[{][A-Za-z-_]*?[\]}]', '{}', api_call['path'])
        api_path = api_path.format(* var_list)
        sample_req = re.sub(r'\'https.*?\'', api_path, sample_req)
        func_desc = '# ' + api_call['gen_func_desc'].replace('\n    ', '\n# ')
        generated_text += make_bash_function(
            api_call['gen_api_name'],
            api_call['gen_params'],
            func_desc,
            sample_req,
        ) + '\n'

    print(generated_text)
    with open('meraki_api.sh', 'w') as myfile:
        myfile.write(generated_text)
    return generated_text
