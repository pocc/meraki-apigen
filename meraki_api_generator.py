# -*- coding: utf-8 -*-
"""Generator for Meraki API python module"""
import json
import re
import textwrap
import datetime
import collections

import requests
import yapf

from _keys import api_key, org_id
from _version import __version__
base_url = 'https://api.meraki.com/api/v0'


headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json',
}


def get_function_text(func_name, func_desc, func_params,
                      req_http_type, req_url_format, req_data):
    """Should work for HTTP GET"""
    if req_data:  # If data field exists, then add a comma for requests call.
        req_data += ', '
    func_param_text = ''
    if func_params:
        func_param_text = ', '.join(func_params)
    max_docstring_first_line_length = 72 - 10  # recommended 72 - both """
    if len(func_desc) > max_docstring_first_line_length:
        func_desc = textwrap.wrap(func_desc, 68)  # recommended 72 - indent
        func_desc = '\n    '.join(func_desc)
    function_text = """\ndef {0}({1}):
    \"\"\"{2}.\"\"\"
    response = requests.{3}(base_url + {4},{5} headers=headers)
    return json.loads(response.text)\n\n""".format(
        func_name,
        func_param_text,
        func_desc,
        req_http_type,
        req_url_format,
        req_data
    )
    return function_text


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


def get_formatted_url(api_call_path):
    """Format the URL string for use in the end function.

    Get the URL string such that parameters passed in can be sent in the
    request by adding them with string.format() in the end function."""
    # The variables that will end up being in the function
    func_vars = ', '.join(re.findall(r'[\[{]([A-Za-z_]*)[\]}]', api_call_path))
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


def make_python():
    """Make python script."""
    # Idea is to have a class per Meraki section.
    api_calls = get_meraki_apidocs_json()
    todays_date = datetime.datetime.now().isoformat()
    http_stats = get_http_stats(api_calls)
    generated_text = """# -*- coding: utf-8 -*-
\"\"\"Generated and linted at {}
Pulled via the Meraki API v0 (https://dashboard.meraki.com/api_docs/)
API calls: {} {} 

Meraki API Generator v{}
    Convert all of the recently released API calls into Python function calls.
    As new API calls are released all the time, rerun this occasionally.

More Info
    Contact: Ross Jacobs (rosjacob [AT] cisco.com)
    Github: https://github.com/pocc/meraki-apigen
    Issues: https://github.com/pocc/meraki-apigen/issues
\"\"\"
import json\nimport requests
base_url = 'https://api.meraki.com/api/v0'
headers = {{
    'X-Cisco-Meraki-API-Key': '{}',
    'Content-Type': 'application/json'
}}\n\n""".format(todays_date, len(api_calls), http_stats, __version__, api_key)
    api_call_names = {}
    i = 0
    for api_call in api_calls:
        i += 1
        api_call_name = generate_api_call_name(
            api_call['http_method'], api_call['path'])
        api_call_names[api_call_name] = api_call['description']
        if api_call['http_method'] == 'GET':
            data = ''
        else:
            data = ''

        api_path = re.sub(r'/([A-Za-z_]*?)/\[id\]', r'/[\1_id]',
                          api_call['path'])
        params = get_params(api_call, api_path)
        url_format = get_formatted_url(api_path)
        if api_call['http_method'] == 'GET':
            generated_text += get_function_text(
                func_name=api_call_name,
                func_desc=api_call['description'],
                func_params=params,
                req_http_type=api_call['http_method'].lower(),
                req_url_format=url_format,
                req_data=data)
    linted_text = yapf.yapf_api.FormatCode(
        unformatted_source=generated_text,
        style_config='pep8',
        verify=True
    )[0]
    with open('meraki_api.py', 'w') as myfile:
        myfile.write(linted_text)
    print(linted_text)


def main():
    """Main func."""
    make_python()


if __name__ == '__main__':
    main()
