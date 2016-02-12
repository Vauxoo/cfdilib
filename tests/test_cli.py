#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdicli` module.
"""

import click
from click.testing import CliRunner

import unittest
from os.path import join, dirname

import cfdilib
from cfdilib.cfdicli import cli


class TestCFDIcli(unittest.TestCase):

    def _get_test_data_path(self, file_name):
        return join(self.test_data_dir, file_name)

    def setUp(self):
        self.test_data_dir = join(dirname(cfdilib.__file__), "..", "tests", "demo")
        pass

    def tearDown(self):
        pass

    def test_001_cli(self):
        '''Validating the cli interface works as expected, correctly and with errored files'''

        runner = CliRunner()
        test_path_ok = self._get_test_data_path('basic_invoice_32.txt')
        test_path_nook = self._get_test_data_path('basic_invoice_32_errored.txt')
        result_ok = runner.invoke(cli, ['--in_file', test_path_ok, '--out_file',
                                        '/tmp/document_ok.xml', 'cfdv32mx'])
        result_nook = runner.invoke(cli, ['--in_file', test_path_nook, '--out_file',
                                          '/tmp/document_nook.xml', 'cfdv32mx'])
        #TODO: PASS CORRECT PARAMETERS TO BRING A GREEN
        self.assertTrue(result_ok.output.find('has been created') > 0,
                        'Output from cli different from expected when test file Ok.')
        self.assertTrue(result_nook.output.find('Emisor') > 0,
                        'Output from cli different from expected when test file errored.')
