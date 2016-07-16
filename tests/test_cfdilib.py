#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdilib` module.
Tests for `cfdv32` module.
"""

from os.path import join, dirname
import unittest

from cfdilib import cfdilib, cfdv32
from cfdilib.tools import tools


class TestCfdilib(unittest.TestCase):

    def _get_test_file(self, file_name):
        test_data_file = join(self.test_data_dir, file_name)
        with open(test_data_file) as data_file:
            return data_file.read()

    def setUp(self):
        self.test_data_dir = join(
            dirname(cfdilib.__file__), "..", "tests", "demo")
        self.dict_invoice_basic_32 = eval(
            self._get_test_file('basic_invoice_32.txt'))
        self.dict_invoice_basic_32_errored = eval(
            self._get_test_file('basic_invoice_32_errored.txt'))
        self.real_document_xml = join(
            dirname(cfdilib.__file__), "..", "tests", "demo", 'cfdv32.xml')

    def tearDown(self):
        pass

    # def test_001_get_xsd_documentation(self):
    #     """Getting a documentation from a given Clark's Notated xsd element"""
    #     invoice = cfdv32.get_invoice(self.dict_invoice_basic_32)
    #     self.assertTrue(
    #         invoice.get_documentation(
    #             '{http://www.sat.gob.mx/cfd/3}'
    #             'Impuestos').find('impuestos aplicables') > 0,
    #         'Documentation did not returns the expected element')

    def test_002_get_cfd_debugged(self):
        """With a given valid dict an
        invoice object is created in debug_mode"""
        invoice = cfdv32.get_invoice(self.dict_invoice_basic_32,
                                     debug_mode=True)
        self.assertTrue(invoice.document,
                        'A valid dictionary gave error debugged_mode enabled')

    def test_003_get_cfd(self):
        """With a given valid dict an invoice object is created"""
        invoice = cfdv32.get_invoice(self.dict_invoice_basic_32)
        self.assertTrue(invoice.document,
                        'A valid dictionary gave error an error')

    def test_004_get_errored(self):
        """With a given invalid dict raise properly errors on ups object"""
        invoice = cfdv32.get_invoice(self.dict_invoice_basic_32_errored)
        self.assertTrue(bool(invoice.ups),
                        'An invalid dictionary gave a '
                        'valid output, that is wrong.')
        # Ok it failed!, then we assert if
        # the message is the one I expected for.
        self.assertTrue(invoice.ups.message.find('Emisor') > 0,
                        'The expected failed entry Emisor was erroneous.')

        invoice = cfdv32.get_invoice({})
        self.assertTrue(bool(invoice.ups),
                        'An empty dict should give me the validation')

    def test_005_get_cfd_invalid_debugged(self):
        """With a given `invalid` dict an invoice
        object is created in debug_mode"""
        invoice = cfdv32.get_invoice(
            self.dict_invoice_basic_32_errored, debug_mode=True)
        self.assertTrue(invoice.document,
                        'A invalid dictionary gave error debugged_mode '
                        'enabled gave an error.')

    def test_006_download_file(self):
        """With a file it is downloaded and cached in a temporary file"""
        # TODO: Mock this
        downloaded = tools.cache_it(
            'http://www.sat.gob.mx/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')  # noqa
        content = open(downloaded).read()
        self.assertTrue(content.find('se establece que la salida') > 0,
                        'I read the content of a cached file and '
                        'the result was not correct.')

    def test_006_xml2xslt(self):
        """With a file it is downloaded and cached in a temporary file"""
        # TODO: Mock this
        downloaded = tools.cache_it(
            'http://www.sat.gob.mx/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')  # noqa
        content_xslt = downloaded
        content_xml = self.real_document_xml
        converted = tools.get_original(content_xml, content_xslt)
        self.assertTrue(
            converted,
            'I read the content of a cached file and the result '
            'was not correct.')

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
