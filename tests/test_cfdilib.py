#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdilib` module.
Tests for `cfdv32` module.
"""

from os.path import join, dirname, isfile
from os import environ, unlink
import unittest

from cfdilib import cfdilib, cfdv32
from cfdilib.tools import tools


class TestCfdilib(unittest.TestCase):

    def _get_test_file(self, file_name):
        test_data_file = join(self.test_data_dir, file_name)
        with open(test_data_file) as data_file:
            return data_file.read()

    def setUp(self):
        self.test_url_plain = 'http://www.textfiles.com/ufo/bc_grav1.txt'
        self.s3_url_plain = 'http://s3.vauxoo.com/ufo/bc_grav1.txt'
        # This is the xslt original in order to force the saving recursive in
        # amazon s3 when local.
        self.cadena = 'http://www.sat.gob.mx/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt'
        self.cadena_travis = tools.s3_url('http://s3.vauxoo.com/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')
        self.test_data_dir = join(
            dirname(cfdilib.__file__), "..", "tests", "demo")
        self.dict_invoice_basic_32 = eval(
            self._get_test_file('basic_invoice_32.txt'))
        self.dict_invoice_basic_32_errored = eval(
            self._get_test_file('basic_invoice_32_errored.txt'))
        self.dict_invoice_basic_32_false = eval(
            self._get_test_file('basic_invoice_32_false.txt'))
        self.dict_invoice_basic_32_norfc = eval(
            self._get_test_file('basic_noRFC.txt'))
        self.dict_coa = eval(
            self._get_test_file('coa.txt'))
        self.dict_balance = eval(
            self._get_test_file('balance.txt'))
        self.dict_moves = eval(
            self._get_test_file('moves.txt'))
        self.real_document_xml = join(
            dirname(cfdilib.__file__), "..", "tests", "demo", 'cfdv32.xml')
        self.test_plain = join(
            dirname(cfdilib.__file__), "..", "tests", "demo", "hello.txt")

    def tearDown(self):
        pass

    def test_001_get_xsd_documentation(self):
        """Getting a documentation from a given Clark's Notated xsd element"""
        invoice = cfdv32.get_invoice(self.dict_invoice_basic_32)
        documentation = invoice.get_documentation(
                '{http://www.sat.gob.mx/cfd/3}'
                'Impuestos')
        self.assertTrue(True)  # TODO: Find the proper search element syntax

    def test_002_get_cfd_debugged(self):
        """With a given valid dict an
        invoice object is created in debug_mode"""
        invoice = cfdv32.get_invoice(self.dict_invoice_basic_32,
                                     debug_mode=True)
        self.assertFalse(bool(invoice.ups),
                         'A valid dictionary gave error debugged_mode enabled %s' % invoice.document)
        self.assertTrue(invoice.document,
                        'A valid dictionary gave error debugged_mode enabled')

    def test_002_get_coa(self):
        """With a given valid dict an
        invoice object is created in debug_mode"""
        coa = cfdv32.get_coa(self.dict_coa,
                             debug_mode=True)
        self.assertTrue(coa.document,
                        'A valid dictionary gave error with the coa')
        self.assertFalse(bool(coa.ups),
                         'A valid dictionary gave error coa %s' % coa.document)

    def test_002_get_balance(self):
        """With a given valid dict an
        invoice object is created in debug_mode"""
        balance = cfdv32.get_balance(self.dict_balance,
                                     debug_mode=True)
        self.assertFalse(bool(balance.ups),
                         'A valid dictionary gave error coa %s' % balance.document)
        self.assertTrue(balance.document,
                        'A valid dictionary gave error with the coa')

    def test_002_get_moves(self):
        """With a given valid dict an
        invoice object is created in debug_mode"""
        moves = cfdv32.get_moves(self.dict_moves,
                                 debug_mode=True)
        self.assertFalse(bool(moves.ups),
                         'A valid dictionary gave error coa %s' % moves.document)
        self.assertTrue(moves.document,
                        'A valid dictionary gave error with the coa')

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
                        'The expected failed entry Emisor was erroneous. %s' % invoice.ups.message)

        invoice = cfdv32.get_invoice({})
        self.assertTrue(bool(invoice.ups),
                        'An empty dict should give me the validation')

        invoice = cfdv32.get_invoice(self.dict_invoice_basic_32_false)
        self.assertNotIn('False', invoice.ups.message,
                         'Passing a False value return a False string which is'
                         'incorrect  %s ' % invoice.ups.message)

    def test_005_get_cfd_invalid_debugged(self):
        """With a given `invalid` dict an invoice
        object is created in debug_mode"""
        invoice = cfdv32.get_invoice(
            self.dict_invoice_basic_32_errored, debug_mode=True)
        self.assertTrue(invoice.document,
                        'A invalid dictionary gave error debugged_mode '
                        'enabled gave an error.')

    def test_005_get_norfc(self):
        """With a given `invalid` dict an invoice
        object is created in debug_mode"""
        invoice = cfdv32.get_invoice(
            self.dict_invoice_basic_32_norfc, debug_mode=True)
        self.assertTrue(invoice.document,
                        'A invalid dictionary gave error debugged_mode '
                        'enabled gave an error.')
        self.assertTrue(bool(invoice.ups),
                        'Error expected and not received.')
        self.assertTrue(invoice.ups.message.find('rfc') >= 0,
                        'Expected a controlled error mentioning RFC and gotten other thing.')

    def test_006_download_file(self):
        """With a file it is downloaded and cached in a temporary file"""
        # TODO: Mock this
        downloaded = tools.cache_it(self.cadena_travis)
        content = open(downloaded).read()
        self.assertTrue(content.find('se establece que la salida') > 0,
                        'I read the content of a cached file and '
                        'the result was not correct.')

    def test_007_cache(self):
        """With a file it is downloaded and cached in a temporary file"""
        # TODO: Mock this
        downloaded = tools.cache_it(self.cadena_travis)
        hits = tools._cache_it.cache_info().hits
        new_downloaded = tools.cache_it(self.cadena_travis)
        new_hits = tools._cache_it.cache_info().hits
        self.assertEqual(new_hits - hits, 1,
                         'Cache was not cached properly')
        self.assertEqual(downloaded, new_downloaded, 'Cache different values')
        self.assertTrue(isfile(downloaded), 'Cache was not generate file')

    def test_007_clear_cache(self):
        """With a cached tempfile deleted"""
        # TODO: Mock this
        downloaded = tools.cache_it(self.cadena_travis)
        unlink(downloaded)
        tools.cache_it(self.cadena_travis)
        hits = tools._cache_it.cache_info().hits
        self.assertFalse(hits, 'Cache was not cleared')
        tools.cache_it(self.cadena_travis)
        hits = tools._cache_it.cache_info().hits
        self.assertTrue(hits == 1, 'Cache hits not increased 1 after cleared')

    def test_008_s3(self):
        """Cache on amazon is working properly"""
        if not environ.get('TRAVIS') == 'true':
            # This set of tests can be run just locally with properly set
            # amazon credentials, this will synchronize the xsd files
            # (and others) it does not make sense in travis.
            url = self.test_url_plain
            url_on_s3 = self.s3_url_plain
            new_url = tools.cache_s3(url, self.test_plain)
            self.assertEqual(new_url, url_on_s3,
                             'The url on amazon was not setted properly '
                             'got %s' % new_url)
            new_url = tools.cache_s3(url_on_s3, self.test_plain)
            self.assertEqual(new_url, url_on_s3,
                             'The url on amazon wired not return what I expected'
                             ' properly got %s' % new_url)

            check_s3 = tools.check_s3('NOTEXISTSORNOTPROPERACL', 'url/no/exists')
            self.assertFalse(check_s3, 'checking a non existing bucket fails')
            check_s3 = tools.check_s3('s3.vauxoo.com', 'url/no/exists')
            self.assertFalse(check_s3, 'checking a non existing element fails')

    def test_008_force_s3_creation(self):
        """Updating XSD of CFDIv32 Only local ignored in travis"""
        # Moved to script in root folder.
        pass


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
