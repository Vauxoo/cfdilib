# -*- coding: utf-8 -*-
import os
from abc import ABCMeta, abstractmethod
from tempfile import NamedTemporaryFile
from lxml import etree
from jinja2 import Environment, PackageLoader


class BaseInvoice:
    """Meta model for an invoice, this is the one that will be used To simplify
    the conversion, I will use odoo's attribute names. For an invoice, but we
    should map them with official elements name also in order to be more
    generic this is a TODO.

    Attributes:
        emitted_place Known in the doc as LugarExpedicion format: 'City Name
        State Name, Country'
    """
    __metaclass__ = ABCMeta
    output_file = NamedTemporaryFile(delete=False)
    input_file = NamedTemporaryFile(delete=False)

    def guess_autoescape(self, template_name):
        if template_name is None or '.' not in template_name:
            return False
        ext = template_name.rsplit('.', 1)[1]
        return ext in ('html', 'xhtml', 'htm', 'xml')

    @abstractmethod
    def set_schema(self, schema_fname):
        testxml = os.path.join(os.path.dirname(__file__),
                               'templates', schema_fname)
        with open(testxml, 'r') as element:
            schema = element.read()
        return schema

    @abstractmethod
    def set_template(self, template_fname):
        env = Environment(loader=PackageLoader('cfdilib', 'templates'),
                          extensions=['jinja2.ext.autoescape'],
                          autoescape=self.guess_autoescape)
        return env.get_template(template_fname)

    def validate(self, schema_str, xml_valid):
        """Files path, when any doubt why a path and not a string.
        `http://lxml.de/FAQ.html#why-can-t-lxml-parse-my-xml-from-unicode-strings`
        """
        schema_root = etree.XML(schema_str)
        schema = etree.XMLSchema(schema_root)
        xmlparser = etree.XMLParser(schema=schema)
        try:
            etree.fromstring(xml_valid, xmlparser)
            return True
        except etree.XMLSchemaError:
            return False


class Invoice32(BaseInvoice):
    """An invoice object following 3.2 CFDI legal format.
    """

    def __init__(self, dict_invoice):
        self.set_template_fname()
        self.set_schema_fname()
        self.set_template(self.template_fname)
        self.set_schema(self.schema_fname)
        self.set_cfd()

    def set_template_fname(self):
        """Wired to a known file it works as an API."""
        self.template_fname = 'cfdv32.xml'

    def get_template_fname(self):
        return self.template_fname

    def set_schema_fname(self):
        """The same than template but with .xsd on templates folder."""
        self.schema_fname = self.template_fname.replace('.xml', '.xsd')

    def get_schema_fname(self):
        return self.schema_fname

    def set_template(self, template_fname):
        self.template = super(Invoice32, self).set_template(template_fname)

    def get_template(self):
        return self.template

    def set_schema(self, schema_fname):
        self.schema = super(Invoice32, self).set_schema(schema_fname)

    def get_schema(self):
        return self.schema

    def set_cfd(self):
        """cfd: xml just rendered to be signed."""
        self.cfd = ''

    def get_cfd(self):
        """cfd: xml just rendered to be signed."""
        return self.cfd
