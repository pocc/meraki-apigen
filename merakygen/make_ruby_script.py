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
"""Generate ruby script."""
import re
import textwrap
import os


def make_ruby_function(func_name, func_desc, func_args,
                       req_http_type, req_path):
    """Generate a ruby function given the paramaters."""
    ruby_indented_func_desc = func_desc

    params_should_be_in_url = req_http_type in ['GET', 'DELETE']
    if func_args:  # If there is more than the function description, +newline
        func_desc += '\n    '
    if 'params' in func_args:
        func_args = func_args.replace('params', 'params={}')
        if params_should_be_in_url:
            func_urlencoded_query = '  url_query = URI::encode(params)\n'
            req_path += "#{url_query}"
            # Add additional format variable for params arg to be sent in
            req_data = '[]'
        else:  # req_http_type in ['PUT', 'POST'], data in requests body
            func_urlencoded_query = ''
            req_data = 'params.to_json'
    else:
        func_urlencoded_query = ''
        req_data = '[]'
    for arg in func_args.split(', '):
        infix_arg = '#{' + arg + '}'
        req_path = re.sub(r'\[[a-zA-z-_]*?\]', infix_arg, req_path, count=1)
    if func_args:  # Don't add parentheses if no args (ruby syntactic sugar)
        func_args = '(' + func_args + ')'  # get_orgs() => get_orgs
    function_text = """
{0}
def {1}{2}
{3}  api_call('{4}', "#{{$base_url}}{5}", {6})
end""".format(
        ruby_indented_func_desc,
        func_name,
        func_args,
        func_urlencoded_query,
        req_http_type.upper(),
        req_path,
        req_data
    )
    return function_text


def make_yard_docstring(description, args, link, params,
                        return_type, return_string):
    """Generate a yard doc for a function.

    See https://gist.github.com/chetan/1827484#methods
    Using:
        @param: For regular arg
        @option: For arg in the params variable
        @see: For links
        @example: For the sample resp provided by API docs
        @return: For return value type

    Args:
        description (string): One or two sentence description of function
        args (dict): All arguments and their descriptions
        link (str): Link to the API call
        params (dict): Additional options for this function
        return_type (str): Type of object that function returns
        return_string (str): Any additional context to the return value

    Returns:
        Yard-style docstring
    """
    ruby_docstring_width = 120 - len('# ')
    # Translate all variable names into camelCase

    def my_textwrap(text, indent=2):
        """Wrap text with specific settings."""
        text_lines = text.splitlines()
        wrapped_lines = []
        for line in text_lines:
            wrapped_lines += textwrap.wrap(line,
                                           width=ruby_docstring_width,
                                           expand_tabs=True,
                                           tabsize=2,
                                           replace_whitespace=False,
                                           subsequent_indent=indent*' ')
        return '\n'.join(wrapped_lines)

    if description[-1] != '.':
        description += '.'
    description = my_textwrap(description)

    func_docstring = description + '\n'
    if link:
        func_docstring += '\n@see ' + link

    args_docstring = ''
    for arg in args:
        args_docstring += '\n@param ' + arg + ' [String] ' + args[arg]
    args_docstring = my_textwrap(args_docstring)
    func_docstring += '\n' + args_docstring

    if params:
        for param in params:
            if type(params[param]) == dict:  # Nested params
                func_docstring += '\n@option ' + param + ' [List] ' + \
                    params[param]['description']
                for nested_param in params[param]['options']:
                    np_line = '  @nestedoption ' + nested_param + ' ' \
                              + params[param]['options'][nested_param]
                    func_docstring += '\n' + my_textwrap(np_line, indent=4)
            else:
                param_line = '@option ' + param + ' [String] ' + params[param]
                func_docstring += '\n' + my_textwrap(param_line)

    convert_to_ruby_types = {
        'None': 'nil',
        'list': 'Array',
        'dict': 'Hash',
    }
    return_type_str = '\n@return [' + convert_to_ruby_types[return_type] + ']'
    if return_string:
        return_docstring = return_type_str + '\n@example ' + return_string
    else:
        return_docstring = return_type_str
    func_docstring += '\n' + my_textwrap(return_docstring)
    func_docstring = re.sub(r'\n[\s]*↳', '\n   ↳', func_docstring)
    func_docstring = '# ' + func_docstring.replace('\n', '\n# ')

    return func_docstring


class MakeRubyGem:
    """Make a folder that contains the ruby script and supporting files."""
    def __init__(self, gem, script_text):
        self.gem_name = gem
        self.script_text = script_text

        self.make_gem_scaffolding()
        self.save_static_files()
        self.save_script()

    def make_gem_scaffolding(self):
        """Make the gem directory structure."""
        folders = [self.gem_name]
        for folder in folders:
            if not os.path.isdir(folder):
                os.makedirs(folder)

    def save_static_files(self):
        """Save supporting files like .rubocop.yml."""
        rubocop_text = """AllCops:\n  TargetRubyVersion: 2.3.3"""
        with open(self.gem_name + '/.rubocop.yml', 'w') as myfile:
            myfile.write(rubocop_text)

    def save_script(self):
        """Save all files."""
        with open(self.gem_name + '/' + self.gem_name + '.rb', 'w') as myfile:
            print('\t- saving ' + self.gem_name + '...')
            myfile.write(self.script_text)


def make_ruby_script(api_key, api_calls, preamble, options):
    """Make ruby script."""
    # Indent preamble heredoc exactly 2 spaces
    preamble = '  ' + re.sub(r'\n[ ]*', '\n  ', preamble)
    gem_name = 'pacg_meraki'
    generated_text = """\
<<~HEREDOC
{}
HEREDOC

require 'net/http'
require 'uri'
require 'json'

$base_url = 'https://api.meraki.com/api/v0'

# From Ruby docs. One redirect is expected: a second is not.
def api_call(http_method, url, options, limit = 2)
  raise ArgumentError, 'too many HTTP redirects' if limit.zero?

  uri = URI.parse(url)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  case http_method
  when 'GET' then
    request = Net::HTTP::Get.new(uri.request_uri)
  when 'POST' then
    request = Net::HTTP::Post.new(uri.request_uri)
    request.body = options.to_json
  when 'PUT' then
    request = Net::HTTP::Put.new(uri.request_uri)
    request.body = options.to_json
  when 'DELETE' then
    request = Net::HTTP::Delete.new(uri.request_uri)
  else
    raise ArgumentError, 'Invalid HTTP method'
  end
  request['Content-Type'] = 'application/json'
  request['X-Cisco-Meraki-Api-Key'] = '{}'
  request['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
  response = http.request(request)

  case response
  when Net::HTTPSuccess then
    response.body
  when Net::HTTPRedirection then
    api_call(http_method, response['location'], options, limit - 1)
  else
    response.value
  end
end

""".format(preamble, api_key)
    if options:
        print("WARNING: Ruby options currently won't do anything.")
    whitespace_between_functions = '\n\n'
    sample_resp = ''
    for api_call in api_calls:
        if '--sample-resp' in options:
            sample_resp = api_call['sample_resp']
        api_call_func_desc = make_yard_docstring(
                api_call['func_desc'],
                api_call['func_args'],
                api_call['func_link'],
                api_call['func_params'],
                api_call['func_return_type'],
                sample_resp)
        generated_text += make_ruby_function(
            func_name=api_call['gen_name'],
            func_desc=api_call_func_desc,
            func_args=api_call['gen_func_args'],
            req_http_type=api_call['http_method'],
            req_path=api_call['path']) \
            + whitespace_between_functions
    MakeRubyGem(gem='pacg_meraki', script_text=generated_text)
    print("\nRuby module generated!")
