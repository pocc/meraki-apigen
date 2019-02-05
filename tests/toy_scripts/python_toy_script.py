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
"""Test generated python scripts.

Pylint disable (invalid-name) pylint doesn't like the fact that unittest uses
camel case. As this is an external library, ignore this check.
"""
import unittest
import json

import generated.meraki_api as api

with open('../_apikey') as myfile:
    APIKEY = myfile.read()
with open('../_vars.json') as myfile:
    VARS = json.load(myfile)
api.HEADERS['X-Cisco-Meraki-API-Key'] = APIKEY
# pylint: disable=C0103


class TestApigenDashboard(unittest.TestCase):
    """Test Meraki Apigen for Dashboard."""
    def setUp(self):
        self.maxDiff = None

    def test_get_orgs(self):
        """Get the organizations as a list."""
        org_data = api.get_orgs()
        print(org_data)
        self.assertListEqual(org_data, VARS['ORG_DATA'])

    def test_get_networks(self):
        """Get networks as a list."""
        network_data = api.get_networks_by_org_id(VARS['ORG_ID'])
        print("Network Data:", network_data)
        self.assertListEqual(VARS['NETWORK_DATA'], network_data)

    def test_create_delete_networks(self):
        """Create and delete networks, testing expected output along the way"""
        local_network_data = VARS['NEW_NETWORK_DATA']
        local_new_network = api.create_network_by_org_id(
            VARS['ORG_ID'], VARS['NEW_NETWORK_PARAMS'])
        new_network_id = local_new_network['id']
        # Set ID of the last network to the correct one based on new network.
        local_network_data[-1]['id'] = new_network_id
        remote_all_networks = api.get_networks_by_org_id(VARS['ORG_ID'])
        remote_new_network = remote_all_networks[-1]
        self.assertListEqual(remote_all_networks, local_network_data)
        self.assertDictEqual(remote_new_network, local_new_network)

        code = api.delete_network_by_network_id(new_network_id)
        self.assertEqual(code, 204)

    def test_update_update_networks(self):
        """Change network and change back and verify changes."""
        expected_updated_network = VARS['UPDATED_NETWORK_JSON']
        remote_updated_network = api.update_network_by_network_id(
            VARS['NETWORK_ID'], params={"tags": " west "})
        self.assertDictEqual(expected_updated_network, remote_updated_network)
        remote_updated_network = api.update_network_by_network_id(
            VARS['NETWORK_ID'], params={"tags": ""})
        expected_updated_network['tags'] = ""
        self.assertDictEqual(expected_updated_network, remote_updated_network)

    def test_delete_networks(self):
        """Test deletion of networks (doubles as a network deletion utility)

        network_id='' should return 404.
        An actual network_id should return 204
        """
        network_id = 'N_'
        code = api.delete_network_by_network_id(network_id)
        self.assertEqual(204, code)
        if network_id == 'N_':
            self.assertEqual(404, code)
        else:
            self.assertEqual(204, code)


class TestApigenAdmins(unittest.TestCase):
    """Test Meraki Apigen for Admins."""
    def setUp(self):
        self.maxDiff = None

    def test_get_admins(self):
        """Get a list of admins and compare to expected."""
        actual_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        # lastActive changes all the time. Delete it from the fetched data.
        for index, _ in enumerate(actual_admin_data):
            actual_admin_data[index]['lastActive'] = ""
        print("Expected Data:", VARS['ADMIN_DATA'])
        print("Admin Data:", actual_admin_data)
        self.assertListEqual(VARS['ADMIN_DATA'], actual_admin_data)

    def test_create_delete_admin(self):
        """Create a new admin and then delete them.
        Note this new admin is not a verified admin. Verify admin data before
        and after each API call.
        """
        # Load dicts from store so we can change them.
        expected_new_admin = VARS['NEW_ADMIN']
        expected_new_admin_data = VARS['NEW_ADMIN_DATA']
        new_admin = api.create_admin_by_org_id(VARS['ORG_ID'],
                                               expected_new_admin)
        new_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        # New administrators get new IDs, so add the new ID to local admin dict
        expected_new_admin['id'] = new_admin['id']
        # lastActive changes all the time. Delete it from the fetched data.
        for index, _ in enumerate(new_admin_data):
            new_admin_data[index]['lastActive'] = ""
        # New admin was last added to admin list.
        expected_new_admin_data[-1] = expected_new_admin
        self.assertDictEqual(expected_new_admin, new_admin)
        self.assertListEqual(expected_new_admin_data, new_admin_data)

        code = api.delete_admin_by_admin_id(VARS['ORG_ID'],
                                            expected_new_admin['id'])
        self.assertEqual(code, 204)  # 204 is expected DELETE success.
        new_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        # lastActive changes all the time. Delete it from the fetched data.
        for index, _ in enumerate(new_admin_data):
            new_admin_data[index]['lastActive'] = ""
        self.assertListEqual(new_admin_data, VARS['ADMIN_DATA'])

    def test_delete_admin(self):
        """Test deletion of networks (doubles as a network deletion utility)

        admin_id=0 should return 404. Real admin_id should return 204"""
        admin_id = 0
        code = api.delete_admin_by_admin_id(VARS['ORG_ID'], admin_id)
        if admin_id == 0:
            self.assertEqual(404, code)
        else:
            self.assertEqual(204, code)

    def test_delete_extra_admin(self):
        """If there's one more admin than expected, delete them."""
        actual_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        # lastActive changes all the time. Delete it from the fetched data.
        for index, _ in enumerate(actual_admin_data):
            actual_admin_data[index]['lastActive'] = ""
        actual_ids = [admin['id'] for admin in actual_admin_data]
        expected_ids = [admin['id'] for admin in VARS['ADMIN_DATA']]
        if actual_ids != expected_ids:
            diff_admin_id = list(set(actual_ids).difference(
                set(expected_ids)))[0]
            diff_admin_email = [admin['email'] for admin in actual_admin_data
                                if admin['id'] == diff_admin_id][0]
            print("Deleting admin...\nemail:", diff_admin_email,
                  "\nID:", diff_admin_id)
            code = api.delete_admin_by_admin_id(VARS['ORG_ID'], diff_admin_id)
            print("Return code is ", code)
        else:
            print("No excess admins detected!")
