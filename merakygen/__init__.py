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
"""Package merakygen."""
import re

__version__ = '0.2.0'
__description__ = 'Generate a module to access the Meraki API in $language'
__project_url__ = 'https://github.com/pocc/merakygen'


def format_changelog():
    """Get formatted text from the changelog that looks better in a cli."""
    with open('../CHANGELOG.md') as file_obj:
        changelog = file_obj.read()
    # Delete headings and indent bullet points.
    changelog = changelog.replace('###', ' ').replace('\n*', '\n\t*')
    get_release_text_regex = r'.*?(\[[\d]+\.[\d]+\.[\d]+\][\S\s]*?)\n## '
    releases = re.findall(get_release_text_regex, changelog)
    releases = releases
    return '\n'.join(releases)


__changelog__ = format_changelog()
