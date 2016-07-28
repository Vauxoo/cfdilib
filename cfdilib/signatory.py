# -*- coding: utf-8 -*-
from __future__ import print_function
from suds.client import Client
from urllib2 import URLError


class Signatory(object):
    """A third party element against which we will sign the invoice.
    In Mexico for example it is called PAC, in Spain is the goverment itself
    In other countries it can be a different entity, private or public and use
    different kind of web services technologies.

    This is an object to be used as a helper, this should be overwritten
    if the way we decided to sign (SOAP, xmlrpc, json, etc, etc)
    change in your country.

    The default behavior is for the way Mexico do things.
    """
    def __init__(self, url, user, password):
        self.message = None
        self.client = None
        self.url = url
        self.user = user
        self.password = password
        self.document = None
        self.result = None

    def _sign(self):
        try:
            # The name of the service here will
            # change depending of the signatory third party.
            self.result = self.client.service.stamp(
                self.document, self.user, self.password)
        except Exception as e:
            print(e)  # pylint: disable=print-statement

    def sign(self, xml_doc):
        """Sign the document with a third party signatory.

        :param str xml_doc: Document self signed in plain xml
        :returns answer: Answer is given from the signatory
            itself if connected.
        """
        try:
            self.client = Client(self.url)
        except ValueError as e:
            self.message = e.message
        except URLError:
            self.message = 'The url you provided: ' + \
                '%s could not be reached' % self.url
