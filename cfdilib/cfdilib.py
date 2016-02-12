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


class BaseDocument:
    """An XML document following any format given an XSD file.
    Due to avoid duplication of work we will delegate the error management
    Of attributes to the xsd, then the `validate` method will make the job of
    return the correct error, due to the standard managend on the invoice.

    The template itself must comply with an specific xsd, this is needed to
    simply pass a dictionary of terms used in the template convert them to
    attributes of this Document object using whatever attributes comes from that xsd

    Then due to the template itself has all the structure of attributes
    necessaries to comply with the xsd, theoretically the xsd should return the
    logical error which we are not complying on such template, see cfdv32.xml template to see
    how you should assembly a new version of this template, then set it to the
    template_fname attribute and guala your dict will be magically validated
    and converted to an XML file.

    Why not assembly with simple lxml?
    ----------------------------------

    Because it is more readable and configurable, it is always more simple
    inherit a class and set an attribute than overwrite hundreds of methods
    when it is a big xml.
    """

    @abstractmethod
    def __init__(self, dict_document, debug_mode=False):
        """Convert a dictionary invoice to a Class

        @param :dict_invoice Dictionary with all entries you will need in your
        template.
        """
        self.debug_mode = debug_mode
        self.set_schema_fname()
        self.set_schema(self.schema_fname)
        self.__dict__.update(dict_document)
        for k, v in dict_document.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

    __metaclass__ = ABCMeta
    output_file = NamedTemporaryFile(delete=False)
    input_file = NamedTemporaryFile(delete=False)
    ups = False

    def set_schema_fname(self):
        """The same than template but with .xsd on templates folder."""
        self.schema_fname = self.template_fname.replace('.xml', '.xsd')

    def guess_autoescape(self, template_name):
        '''Given a template Name I will gues using its extension if we should autoscape or not.
        Defaul autoscaped extensions: ('html', 'xhtml', 'htm', 'xml')
        '''
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

    def validate(self, schema_str, xml_valid):  # TODO: be able to get doc for error given an xsd.
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
            result = True
        except etree.XMLSyntaxError as ups:
            self.ups = ups
            result = False
        finally:
            return result

    def set_xml(self):
        """document xml just rendered already validated against xsd to be signed.

        :params boolean debug_mode: Either if you want the rendered template to be saved either it
        is valid or not with the given schema.

        :returns boolean: Either was valid or not the generated document.
        """
        document = self.template.render(inv=self)
        self.document = False
        if self.debug_mode:
            self.document = document
        if self.validate(self.schema, document):
            self.document = document

    def get_element_from_clark(self, element):
        '''**Helper method:** Given a Clark's Notation `{url:schema}Element` element, return the
        valid xpath on your xsd file, frequently it is not necesary overwrite this method but
        different xsd from different sourcs can have different logic which I do not know now,
        then simply take this as an example and set the correct xpath conversion in your project.

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
