#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_signatory
----------------------------------

Tests for `signatory` module.
"""

import unittest
from cfdilib.signatory import Signatory
import suds


class TestSignatory(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_managing_known_errors(self):
        """Given a malformed url"""
        signatory = Signatory('test', 'test_usr', 'pass_test')
        signatory.sign('<a>XML</a>')
        self.assertTrue(
            signatory.message.find('unknown') >= 0,
            'Passing an incorrect url the message was not the expected')

    def test_002_managing_known_errors(self):
        """Given a well formed url but unkown host"""
        url = 'http://url.do.not.exist.com'
        signatory = Signatory(url, 'test_usr', 'pass_test')
        signatory.sign('<a>XML</a>')
        self.assertTrue(signatory.message.find(url) >= 0,
                        'Passing an incorrect url the message '
                        'was not the expected: %s' % signatory.message)

    def test_003_managing_known_errors(self):
        """Given a well formed url but incorrect user password
        client is setted correctly."""
        # TODO: Mock this test
        url = 'http://demo-facturacion.finkok.com/servicios/soap/stamp.wsdl'
        signatory = Signatory(url, 'xx', 'yy')
        signatory.sign('<a>XML</a>')
        self.assertTrue(isinstance(signatory.client, suds.client.Client),
                        'Passing a correct  url the '
                        'client object is not what I expected')
        self.assertTrue(signatory.message is None,
                        'The message on the invoice object should'
                        ' be False and it is not')
