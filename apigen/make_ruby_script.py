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
"""Generate ruby script.

Does not work.
"""
import subprocess as sp
import re


def get_ruby_versions():
    """Check whether ruby/gem is installed. If so, then rubocop can be used."""
    try:
        sp_ruby_ver = sp.Popen(['ruby', '-v'], stdout=sp.PIPE)
        sp_gem_ver = sp.Popen(['gem', '-v'], stdout=sp.PIPE)
        ruby_ver = sp_ruby_ver.communicate()[0].decode('utf-8')
        gem_ver = sp_gem_ver.communicate()[0].decode('utf-8')
        return re.sub(r'\n|ruby ', '', ruby_ver), re.sub(r'\n', '', gem_ver)
    # If not installed, catch the error and return not found.
    except FileNotFoundError:
        msg = 'not found (required for ruby linting and testing)'
        return msg, msg


def make_ruby_script(api_key, todays_date, num_api_calls, http_stats):
    """Make ruby script."""
    generated_text = """\
<<-HEREDOC

HEREDOC

require 'net/http'
require 'uri'

api_key = {}
"""
    ruby_ver, gem_ver = get_ruby_versions()
    return generated_text


def make_ruby_function(func_name, func_desc, func_params,
                       req_http_type, req_url_format, req_data):
    """Should work for HTTP GET"""
    if req_data:  # If data field exists, then add a comma for requests call.
        req_data += ', '
    function_text = """\
def {}({})
    # {}
    uri = URI.parse("{}")
    request = Net::HTTP::{}.new(uri)
    request.content_type = "application/json"
    request["X-Cisco-Meraki-Api-Key"] = api_key

    req_options = {{
      use_ssl: uri.scheme == "https",
      {}
    }}

    response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
      http.request(request)
    end

    response.code
    response.body
end\n\n""".format(
        func_name,
        func_params,
        func_desc,
        req_url_format,
        req_http_type.lower().capitalize(),  # Needs to be 'Get', 'Put'
        req_data
    )

    return function_text
