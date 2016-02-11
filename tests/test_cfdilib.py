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
            'emitter_street': 'Linuk 119',
            'emitter_zip': '37205',
            'emitter_colony': u'Futurama Monteérrey',
            'emitter_state': u'Guanajuato',
            'emitter_locality': u'Guanajuato',
            'certificate_number': '00001000000301059770',
            'document_type': 'ingreso',
            'approval_number': 'VAU',  # TODO: esto deberia ser simpl serie
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

        invoice = cfdilib.get_invoice(self.dict_invoice_basic)
        # print invoice.get_documentation('municipio')

    def test_002_get_cfd(self):
        invoice = cfdilib.get_invoice(self.dict_invoice_basic)
        # TODO: delete this commented stuff it is just to manage the error.
        # print type(invoice.ups.error_log.filter_from_errors())
        # print dir(invoice.ups.error_log.filter_from_errors())
        # for e in invoice.ups.error_log.filter_from_errors():
        #     print type(e)
        #     print dir(e)
        #     for attt in dir(e):
        #         if not attt.startswith('_'):
        #             print 'attr:   ...   ',attt
        #             print e.__getattribute__(attt)

        self.assertFalse(invoice.ups,
                         'A valid dictionary gave error the error was: %s' % invoice.ups.message)  # noqa


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
