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


def make_ruby_script(api_key, api_calls, preamble, options):
    """Make ruby script."""
    output_file = 'meraki_api.rb'
    generated_text = """\
<<-HEREDOC

HEREDOC

require 'net/http'
require 'uri'
require 'json'

json_file = File.read('_vars.json')
json_vars = JSON.parse(json_file)
$api_key = json_vars["API_KEY"]
$org_id = json_vars["ORG_ID"]
$new_admin = json_vars["NEW_ADMIN"]

base_url = 'https://api.meraki.com/api/v0'


# From Ruby docs. One redirect is expected: a second is not.
def fetch(http_method, site, options, limit = 2)
  raise ArgumentError, 'too many HTTP redirects' if limit.zero?

  uri = URI.parse(site)
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
  request['X-Cisco-Meraki-Api-Key'] = $api_key
  request['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
  response = http.request(request)

  case response
  when Net::HTTPSuccess then
    response.body
  when Net::HTTPRedirection then
    fetch(http_method, response['location'], options, limit - 1)
  else
    response.value
  end
end
""".format(api_key)

    with open(output_file, 'w') as myfile:
        print('\tsaving ' + output_file + '...')
        myfile.write(generated_text)


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
