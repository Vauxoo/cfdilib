#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cfdilib
----------------------------------

Tests for `cfdilib` module.
"""

from os.path import join, dirname
import unittest

from cfdilib import cfdilib


class TestCfdilib(unittest.TestCase):

    def setUp(self):
        # TODO: Put this dict in the testdoc in order to have it automagically
        # documented.
        self.dict_invoice_basic = {
            'emitter_domicile': 'Vauxoo SA de CV',
            'currency': 'MXN',
            'account': '123456',
            'rate': '17.8',
            'certificate': 'CERTIFXSFT',
            'date_invoice_tz': '2016-06-01T06:07:08',
            'number': 'ABC456',
            'emitter_name': 'Vauxoo SA de CV',
            'emitter_rfc': 'VAU111017CG9',
            'emitter_street': 'Lunik 119',
            'emitter_zip': '37205',
            'emitter_colony': u'Futurama Monteérrey',
            'emitter_municipality': u'No se que iria',
            'emitter_state': u'Guanajuato',
            'emitter_locality': u'Guanajuato',
            'emitter_exterior_no': 123,
            'emitter_interior_no': 'N/A',
            'emitter_country': u'México',
            'emitter_issue_on_name': 'Vauxoo SA de CV',
            'emitter_issue_on_rfc': 'VAU111017CG9',
            'emitter_issue_on_street': 'Linuk 119',
            'emitter_issue_on_zip': '37205',
            'emitter_issue_on_colony': u'Futurama Monteérrey',
            'emitter_issue_on_municipality': u'No se que iria',
            'emitter_issue_on_state': u'Guanajuato',
            'emitter_issue_on_locality': u'Guanajuato',
            'emitter_issue_on_exterior_no': 123,
            'emitter_issue_on_interior_no': 'N/A',
            'emitter_issue_on_country': u'México',
            'receiver_name': 'Some Customer SC',
            'receiver_rfc': 'ECI0006019E0',
            'receiver_street': u'Av. Unión',
            'receiver_zip': '44158',
            'receiver_colony': u'Futurama Monteérrey',
            'receiver_municipality': u'No se que iria',
            'receiver_state': u'ECI0006019E0',
            'receiver_locality': u'Col. Deitz',
            'receiver_exterior_no': 125,
            'receiver_interior_no': 'N/A',
            'receiver_country': u'México',
            'certificate_number': '00001000000301059770',
            'emitter_fiscal_position': u'Personas morales del Régimen general',
            'document_type': 'ingreso',
            'approval_number': 'VAU',  # TODO: esto deberia ser simpl serie  # TODO: esto deberia ser simpl serie
            'taxes': {'total_transferred': 0.0,
                      'total_withhold': 0.0,
                      },

        }
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

        invoice = cfdilib.get_invoice(self.dict_invoice_basic)
        self.assertTrue(invoice.validate(invoice.schema,
                                         self._get_test_file('cfdv32.xml')),
                        'The xml can be used with all parameters')
        self.assertTrue(invoice.validate(invoice.schema,
                                         self._get_test_file(
                                             'cfdv32.notaxes.xml')),
                        'The xml can be used with no taxes, just the tag')
        self.assertFalse(invoice.validate(invoice.schema,
                                          self._get_test_file(
                                              'cfdv32.bad.xml')),
                         'The xml bring a fixed attribute incorrectly')
        self.assertFalse(invoice.validate(invoice.schema,
                                          self._get_test_file(
                                              'cfdv32.bad.label.xml')),
                         'The xml bring a not valid attribute')
        self.assertFalse(invoice.validate(invoice.schema,
                                          self._get_test_file(
                                              'cfdv32.bad.schema.xml')),
                         'The xml do not bring any schema compliant')

    def test_001_get_xsd_documentation(self):
        '''Getting a documentation from a given Clark's Notated xsd element'''
        invoice = cfdilib.get_invoice(self.dict_invoice_basic)
        self.assertTrue(invoice.get_documentation('{http://www.sat.gob.mx/cfd/3}Impuestos').find('impuestos aplicables') > 0,
                        'Documentation did not returns the expected element' )



    def test_002_get_cfd(self):
        '''TODO: This test simply will validate that with a given valid dict an invoice object is crated'''
        invoice = cfdilib.get_invoice(self.dict_invoice_basic)
        self.assertFalse(False,  # TODO: here will be invoice.ups
                         'A valid dictionary gave error the error was: %s' % invoice.ups.message)  # noqa


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
