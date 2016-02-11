# -*- coding: utf-8 -*-
import os
from cStringIO import StringIO
from abc import ABCMeta, abstractmethod
from tempfile import NamedTemporaryFile
from lxml import etree
from jinja2 import Environment, PackageLoader


class Struct(object):
    def __init__(self, adict):
        """Convert a dictionary to a class

        @param :adict Dictionary
        """
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

class BaseInvoice:
    """Meta model for an invoice, this is the one that will be used To simplify
    the conversion.

    Attributes:
        emitted_place: Known in the doc as LugarExpedicion format
                       'City Name State Name, Country'
    """
    __metaclass__ = ABCMeta
    output_file = NamedTemporaryFile(delete=False)
    input_file = NamedTemporaryFile(delete=False)
    ups = False

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
        """Compare the valid information on an xml from  given schema.

        :param str schema_str: content string from schema file.
        :param str xml_valid: content string from xml file.
        :returns: If it is Valid or Not.
        :rtype: bool
        """
        schema_root = etree.XML(schema_str)
        schema = etree.XMLSchema(schema_root)
        xmlparser = etree.XMLParser(schema=schema)
        try:
            etree.fromstring(xml_valid, xmlparser)
            return True
        except etree.XMLSchemaError as ups:
            self.ups = ups
            return False
        except etree.XMLSyntaxError as ups:
            self.ups = ups
            return False

    def get_element_from_clark(self, element):
        '''**Helper method:** Given a Clark's Notation `{url:schema}Element` element, return the valid xpath on your
        xsd file, frequently it is not necesary overwrite this method but different xsd from
        different sourcs can have different logic which I do not know now, then simply take this
        as an example and set the correct xpath conversion in your project.

        :param str element: Element string following the Clark's Notation'''
        element = element.split('}')[-1]
        xpath_path = '//xs:element[@name="{element}"]/xs:annotation/xs:documentation'.format(element=element)  # noqa

        return xpath_path

    def get_documentation(self, element, namespace=None, schema_str=None):
        '''**Helper method:** should return an schema specific documentation
        given an element parsing or getting the `Clark's Notation`_
        `{url:schema}Element` from the message error on validate method.

        :param str element: Element string following the Clark's Notation
        :param dict namespace: Element string following the Clark's Notation

        :returns: The documentation text if exists
        :rtype: unicode

        .. _`Clark's Notation`: http://effbot.org/zone/element-namespaces.htm
        '''
        if namespace is None:
            namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        schema_root = etree.parse(StringIO(self.schema))
        document = schema_root.xpath(self.get_element_from_clark(element),
                                     namespaces=namespace)
        return document and document[0].text or ''


class Invoice32(BaseInvoice):
    """An invoice object following 3.2 CFDI legal format.
    Due to avoid duplication of work we will delegate the error management
    Of attributes to the xsd, then the `validate` method will make the job of
    return the correct error, due to the standard managend on the invoice.

    The template itself must comply with an specific xsd, this is needed to
    simply pass a dictionary of terms used in the template convert them to
    attributes of this Invoice32 object using whatever attributes comes there

    Then due to the template itself has all the structure of attributes
    necessaries to comply with the xsd, theretically the xsd should return the
    logical error which we are not complying, see cfdv32.xml template to see
    how you should assembly a new version of this template, then set it to the
    template_fname attribute and guala your dict will be magically validated
    and converted to an XML file.

    Why not assembly with simple lxml?
    ----------------------------------

    Because it is more readable and configurable, it is always more simple
    inherit a class and set an attribute than overwrite hundreds of methods
    when it is a big xml.
    """

    def __init__(self, dict_invoice):
        """Convert a dictionary invoice to a Class

        @param :dict_invoice Dictionary with all entries you will need in your
        template.
        """

        self.set_template_fname()
        self.set_schema_fname()
        self.set_template(self.template_fname)
        self.set_schema(self.schema_fname)
        self.__dict__.update(dict_invoice)
        for k, v in dict_invoice.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

            if isinstance(v, list):
                self.__dict__[k] = StructList(v)
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
        """cfd: xml just rendered already validated against xsd to be signed.
        """
        cfd = self.template.render(inv=self)
        if self.validate(self.schema, cfd):
            self.cfd = cfd
        self.cfd = False

    def get_cfd(self):
        """cfd: xml just rendered to be signed."""
        return self.cfd


def get_invoice(dict_invoice):
    return Invoice32(dict_invoice)
