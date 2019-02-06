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
"""Module to govern interaction with the web."""
import json
import os
import time

import requests


def fetch_apidocs_json():
    """Get all API calls from the docs.

    * apidocs json is shipped with projcet at merakygen/static/api.json
    * This will be used if there is no network connection, but
      may be out-of-date.
    * If this program is run multiple times, try to cache it to
      save on network requests and speed.
    """
    try:
        # If a local copy has been created in the last 24 hours, use it.
        if os.path.exists('api.json') and \
                time.time() - os.stat('api.json').st_mtime > 86400:
            api_docs = get_json_str_from_file('api.json')
        else:
            # Get the json by splitting the pagetext at json beginning and end.
            meraki_apidocs = 'https://dashboard.meraki.com/api_docs'
            pagetext = requests.get(meraki_apidocs).text
            lower_split = pagetext.split("window.allApisJson = ")[1]
            all_api_docs_str = lower_split.split(";\n  </script>")[0]
            # Write the json so a cached version is now available.
            with open('api.json', 'w') as file_obj:
                file_obj.write(all_api_docs_str)
            api_docs = json.loads(all_api_docs_str)
    except requests.exceptions.ConnectionError:
        api_docs = get_json_str_from_file('../static/api.json')

    return api_docs


def get_json_str_from_file(filename):
    """Open a file and get its JSON as a dict."""
    with open(filename) as file_obj:
        return json.loads(file_obj.read())
