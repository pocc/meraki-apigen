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
import yapf


def get_python_func(func_name, func_desc, func_args,
                    req_http_type, req_url_format):
    """Generate a python function given the paramaters."""
    params_should_be_in_url = req_http_type in ['GET', 'DELETE']
    if 'params' in func_args:
        if params_should_be_in_url:
            func_urlencoded_query = """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')"""
            # Add addtional format variable for params arg to be sent in
            req_url_format = req_url_format.replace("\'.format", "{}\'.format")
            assert req_url_format.count(')') < 2  # Should only be format )
            req_url_format = req_url_format.replace(')', ', url_query)')
            req_data = ''
        else:  # req_http_type in ['PUT', 'POST'], data in requests body
            func_urlencoded_query = ''
            req_data = 'data=params, '
    else:
        func_urlencoded_query = ''
        req_data = ''
    function_text = """\ndef {0}({1}):
    \"\"\"{2}.\"\"\"{3}
    response = requests.{4}(base_url + {5},{6} headers=headers)
    return json.loads(response.text)\n\n""".format(
        func_name,
        func_args,
        func_desc,
        func_urlencoded_query,
        req_http_type.lower(),
        req_url_format,
        req_data
    )
    return function_text


def make_python_script(api_key, api_calls, preamble):
    """Make python script."""
    generated_text = """\
# -*- coding: utf-8 -*-
\"\"\"{}\"\"\"
import json\nimport requests\nimport urllib.parse\n
base_url = 'https://api.meraki.com/api/v0'
headers = {{
    'X-Cisco-Meraki-API-Key': '{}',
    'Content-Type': 'application/json'
}}\n\n""".format(preamble, api_key)
    for api_call in api_calls:
        generated_text += get_python_func(
            func_name=api_call['gen_api_name'],
            func_desc=api_call['gen_func_desc'],
            func_args=api_call['gen_args'],
            req_http_type=api_call['http_method'],
            req_url_format=api_call['gen_formatted_url'])
    linted_text = yapf.yapf_api.FormatCode(
        unformatted_source=generated_text,
        style_config='pep8',
        verify=True
    )[0]
    with open('meraki_api.py', 'w') as myfile:
        myfile.write(linted_text)
    print(linted_text)
