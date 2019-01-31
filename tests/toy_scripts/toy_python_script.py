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

import examples.meraki_api as api

with open('_vars.json') as myfile:
    VARS = json.load(myfile)

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

    def util_delete_networks(self):
        """Delete a network manually given a network ID if a test failed."""
        code = api.delete_network_by_network_id(network_id='')
        self.assertEqual(code, 204)


class TestApigenAdmins(unittest.TestCase):
    """Test Meraki Apigen for Admins."""
    def setUp(self):
        self.maxDiff = None

    def test_get_admins(self):
        """Get a list of admins and compare to expected."""
        actual_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        print("Admin Data:", actual_admin_data)
        self.assertListEqual(VARS['ADMIN_DATA'], actual_admin_data)

    def test_add_delete_admin(self):
        """Create a new admin and then delete them.
        Note this new admin is not a verified admin. Verify admin data before
        and after each API call.
        """
        # Load dicts from store so we can change them.
        local_new_admin = VARS['NEW_ADMIN']
        local_new_admin_data = VARS['NEW_ADMIN_DATA']
        new_admin = api.create_admin_by_org_id(VARS['ORG_ID'], local_new_admin)
        current_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        # New administrators get new IDs, so add the new ID to local admin dict
        local_new_admin['id'] = new_admin['id']
        # New admin was last added to admin list.
        local_new_admin_data[-1] = local_new_admin
        self.assertDictEqual(new_admin, local_new_admin)
        self.assertListEqual(current_admin_data, local_new_admin_data)

        code = api.delete_admin_by_admin_id(VARS['ORG_ID'], local_new_admin['id'])
        self.assertEqual(code, 204)  # 204 is expected DELETE success.
        current_admin_data = api.get_admins_by_org_id(VARS['ORG_ID'])
        self.assertListEqual(current_admin_data, VARS['ADMIN_DATA'])

    def test_delete_admin(self):
        """For a random admin ID, the return code should be 404."""
        code = api.delete_admin_by_admin_id(VARS['ORG_ID'], 0)
        self.assertEqual(404, code)
