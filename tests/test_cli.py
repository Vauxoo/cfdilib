#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdicli` module.
"""

import unittest
from os.path import dirname, join
from shutil import copy

from click.testing import CliRunner

import cfdilib
from cfdilib.cfdicli import cli


class TestCFDIcli(unittest.TestCase):

    def _get_test_data_path(self, file_name):
        return join(self.test_data_dir, file_name)

    def setUp(self):
        self.test_data_dir = join(
            dirname(cfdilib.__file__), "..", "tests", "demo")

    def tearDown(self):
        pass

    def test_001_cli(self):
        """The cli interface works as expected,
        with correct and errored files"""

        runner = CliRunner()
        with runner.isolated_filesystem():
            test_path_ok = self._get_test_data_path('basic_invoice_32.txt')
            copy(test_path_ok, 'document.json')
            test_path_nook = self._get_test_data_path(
                'basic_invoice_32_errored.txt')
            result_ok = runner.invoke(
                cli, ['--in_file', test_path_ok, '--out_file',
                      '/tmp/document_ok.xml', 'cfdv32mx'])
            self.assertTrue(
                result_ok.output.find('has been created') > 0,
                'Output from cli different from expected when test file Ok.')
            result_nook = runner.invoke(
                cli, ['--in_file', test_path_nook, '--out_file',
                      '/tmp/document_nook.xml', 'cfdv32mx'])
            self.assertTrue(result_nook.output.find('Emisor') > 0,
                            'Output from cli different from expected when test'
                            ' file errored.')
            result_ok_nofiles = runner.invoke(cli, ['cfdv32mx'])
            self.assertTrue(
                result_ok_nofiles.output.find('has been created') > 0,
                'Output with no files as parameters failed.')
