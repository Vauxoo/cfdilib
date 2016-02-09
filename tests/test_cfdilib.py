#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdilib` module.
"""

from os.path import join, dirname
import unittest

import cfdilib
from cfdilib.cfdilib import Invoice32


class TestCfdilib(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_test_file(self, file_name):
        test_data_dir = join(dirname(cfdilib.__file__), "..", "tests", "demo")
        test_data_file = join(test_data_dir, file_name)
        with open(test_data_file) as data_file:
            return data_file.read()

    def test_000_validator(self):
        """Given a known valid/invalid file asserting with a known xsd"""
        # Force return a know valid xml file.

        invoice = Invoice32({})
        self.assertTrue(invoice.validate(invoice.schema,
                                         self._get_test_file('cfdv32.xml')))


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
