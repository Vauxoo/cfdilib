#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdilib` module.
"""

from os.path import join, dirname
import unittest

from cfdilib import cfdilib, facturaev321


class TestFacturaev321(unittest.TestCase):

    def _get_test_file(self, file_name):
        test_data_file = join(self.test_data_dir, file_name)
        with open(test_data_file) as data_file:
            return data_file.read()

    def setUp(self):
        self.test_data_dir = join(dirname(cfdilib.__file__), "..", "tests", "demo")
        self.dict_invoice_basic_32 = eval(self._get_test_file('basic_facturae_v321.txt'))
        self.dict_invoice_basic_32_errored = eval(self._get_test_file('basic_facturae_v321_errored.txt'))

    def tearDown(self):
        pass

    def test_001_get_xsd_documentation(self):
        '''Getting a documentation from a given Clark's Notated xsd element'''
        invoice = facturaev321.get_invoice(self.dict_invoice_basic_32)
        self.assertTrue(invoice.get_documentation('{http://www.sat.gob.mx/cfd/3}Impuestos')
                        .find('impuestos aplicables') > 0,
                        'Documentation did not returns the expected element')

    def test_002_get_cfd_debugged(self):
        '''validate that with a given valid dict an invoice object is created in debug_mode'''
        invoice = facturaev321.get_invoice(self.dict_invoice_basic_32, debug_mode=True)
        self.assertTrue(invoice.document,
                        'A valid dictionary gave error debugged_mode enabled gave an error.')

    def test_003_get_cfd(self):
        '''validate that with a given valid dict an invoice object is created in debug_mode'''
        invoice = facturaev321.get_invoice(self.dict_invoice_basic_32, debug_mode=False)
        self.assertTrue(invoice.document,
                        'A valid dictionary gave error an error')

    def test_004_get_errored(self):
        '''validate that with a given invalid dict raise properly errors on ups object'''
        invoice = facturaev321.get_invoice(self.dict_invoice_basic_32_errored)

        self.assertTrue(invoice.ups,
                      'An invalid dictionary gave a valid output, that is wrong.')

        # Ok it failed!, then we assert if the message is the one I expected for.

        self.assertTrue(invoice.ups.message.find('Emisor') > 0,
                        'The expected faled entry Emisor was erroneous.')


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
