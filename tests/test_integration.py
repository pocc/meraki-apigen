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
"""Test using mock."""
import unittest
import subprocess as sp
import glob
import os
import importlib

import apigen.__keys as keys
import apigen.make_bash_script as mbs


class TestMerakiApigen(unittest.TestCase):
    """Test Meraki Apigen."""
    def setUp(self):
        """In case tests are started in the tests folder"""
        if os.path.basename(os.getcwd()).startswith('tests'):
            os.chdir('..')
        self.entry_point = 'gateway.py'

    def test_integration_python(self):
        """Test python generation."""
        cmd_list = ['python', self.entry_point, '--key', keys.api_key,
                    '--language', 'python']
        sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
        sp_stdout, sp_stderr = sp_pipe.communicate()
        self.assertIsNone(sp_stderr.decode('utf-8'))
        # Import the file that was just created and get organizations.
        generated = importlib.import_module('meraki_api')
        org_data = generated.get_organizations()
        print("Organizations received with generated file:\n", org_data)
        self.assertEqual(org_data, keys.org_data)
        self.assertIn('meraki_api.py', os.listdir(os.getcwd()))

    def test_integration_bash(self):
        """Test bash geneartion."""
        if mbs.get_bash_version().startswith('not found'):
            # Generate the file and verify that it exsists.
            cmd_list = ['python', self.entry_point, '--key', keys.api_key,
                        '--language', 'python']
            sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
            sp_stderr = sp_pipe.communicate()[1].decode('utf-8')
            self.assertIsNone(sp_stderr)
            self.assertIn('meraki_api.sh', os.listdir(os.getcwd()))

            # Load the functions in the shell script into the shell.
            cmd_list = ['source', 'apigen/meraki_api.sh']
            sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
            sp_stderr = sp_pipe.communicate()[1].decode('utf-8')
            self.assertIsNone(sp_stderr)

            # Call get_organizations and verify data.
            cmd_list = ['get_organizations']
            sp_pipe = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
            org_data = sp_pipe.communicate()[0].decode('utf-8')
            self.assertEqual(org_data, keys.org_data)

        else:
            print("bash not found. Skipping test_integration_bash.")

    def tearDown(self):
        """Remove any generated modules."""
        for file in glob.glob("meraki_api.*"):
            os.remove(file)
