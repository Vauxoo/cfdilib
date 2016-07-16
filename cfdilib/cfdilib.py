# -*- coding: utf-8 -*-
import os
from os.path import dirname
from cStringIO import StringIO
from abc import ABCMeta, abstractmethod
from tempfile import NamedTemporaryFile

from lxml import etree
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import UndefinedError

from .tools import tools


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
    Due to avoid duplication of work we will delegate the
    error management of attributes to the xsd, then the
    `validate` method will make the job of return the correct
    error, due to the standard managed on the invoice.

    The template itself must comply with an specific xsd,
    this is needed to simply pass a dictionary of terms used in
    the template convert them to
    attributes of this Document object using whatever attributes
    comes from that xsd

    Then due to the template itself has all the structure of
    attributes necessaries to comply with the xsd, theoretically
    the xsd should return the logical error which
    we are not complying on such template, see cfdv32.xml
    template to see how you should assembly a new version
    of this template, then set it to the template_fname attribute
    and guala your dict will be magically validated
    and converted to an XML file.

    Why not assembly with simple lxml?
    ----------------------------------

    Because it is more readable and configurable,
    it is always more simple
    inherit a class and set an attribute than overwrite
    hundreds of methods when it is a big xml.
    """

    @abstractmethod
    def __init__(self, dict_document, debug_mode=False, cache=1000):
        """Convert a dictionary invoice to a Class with a
        based xsd and xslt element to be signed.

        :param dict dict_document: Dictionary with all entries
            you will need in your template.
        :param bool debug_mode: If debugging or not.
        :param int cache: Time in seconds the url given
            files will be cached on tmp folder.
        """
        self.ups = False
        self.debug_mode = debug_mode
        self.schema_url = None
        self.document = None
        self.document_path = None
        self.xslt_path = None
        self.xslt_document = None
        self.set_schema_fname()
        self.set_schema(self.schema_fname)
        self.__dict__.update(dict_document)
        for k, v in dict_document.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)
        self.set_xml()
        self.set_xslt_fname()
        self.document_orginal = self.set_original()
        self.template_fname = ''
        self.schema_fname = self.template_fname.replace('.xml', '.xsd')
        self.xslt_fname = self.template_fname.replace('.xml', '.xslt')
        self.templates = os.path.join(dirname(__file__), 'templates')

    __metaclass__ = ABCMeta

    def set_original(self):
        if self.document_path and self.xslt_fname:
            return tools.get_original(self.document_path, self.xslt_fname)

    def set_schema_fname(self):
        """The same than template but with .xsd on templates folder."""
        self.schema_fname = self.template_fname.replace('.xml', '.xsd')

    def set_xslt_fname(self):
        """The same than template but with .xslt on templates
        folder this in case you want to use it locally."""
        if not self.xslt_fname:
            self.xslt_fname = self.template_fname.replace('.xml', '.xslt')
        else:
            self.set_xslt()

    def guess_autoescape(self, template_name):
        """Given a template Name I will gues using its
        extension if we should autoscape or not.
        Default autoscaped extensions: ('html', 'xhtml', 'htm', 'xml')
        """
        if template_name is None or '.' not in template_name:
            return False
        ext = template_name.rsplit('.', 1)[1]
        return ext in ('html', 'xhtml', 'htm', 'xml')

    @abstractmethod
    def set_schema(self, schema_fname):
        test_xml = os.path.join(self.templates, schema_fname)
        with open(test_xml, 'r') as element:
            schema = element.read()
        return schema

    @abstractmethod
    def set_xslt(self):
        if self.xslt_fname and tools.is_url(self.xslt_fname):
            xslt_path = tools.cache_it(self.xslt_fname)
        elif self.xslt_fname:
            xslt_path = os.path.join(self.templates, self.xslt_fname)
        with open(xslt_path, 'r') as element:
            xslt = element.read()
            self.xslt_document = xslt
            # In case of caching,
            # the xslt_path will be from cahed and not from local
            self.xslt_fname = xslt_path

    @abstractmethod
    def set_template(self, template_fname):
        self.templates = os.path.join(dirname(__file__), 'templates')
        env = Environment(loader=FileSystemLoader(self.templates),
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
        # TODO: be able to get doc for error given an xsd.
        schema_root = etree.XML(schema_str)
        schema = etree.XMLSchema(schema_root)
        xmlparser = etree.XMLParser(schema=schema)
        try:
            etree.fromstring(xml_valid, xmlparser)
        except etree.XMLSyntaxError as ups:
            self.ups = ups
        finally:
            if self.ups:
                self.valid = False
            else:
                self.valid = True
            return self.valid

    def set_xml(self):
        """Set document xml just rendered already
        validated against xsd to be signed.

        :params boolean debug_mode: Either if you want
            the rendered template to be saved either it
        is valid or not with the given schema.
        :returns boolean: Either was valid or not the generated document.
        """
        cached = NamedTemporaryFile(delete=False)
        document = u''
        try:
            document = self.template.render(inv=self)
        except UndefinedError as ups:
            self.ups = ups
        valid = self.validate(self.schema, document)
        if not valid and self.debug_mode:
            self.document = document
        if valid:
            document = etree.XML(document)
            self.document = etree.tostring(document,
                                           pretty_print=True,
                                           xml_declaration=True,
                                           encoding='utf-8')
            # TODO: When Document Generated, this this should not fail either.
            # Caching just when valid then.
            with cached as cache:
                cache.write(self.document is not None and self.document or u'')
            self.document_path = cached.name

    def get_element_from_clark(self, element):
        """**Helper method:** Given a Clark's Notation
        `{url:schema}Element` element, return the
        valid xpath on your xsd file, frequently
        it is not necesary overwrite this method but
        different xsd from different source
        can have different logic which I do not know now,
        then simply take this as an example and set the
        correct xpath conversion in your project.

        :param str element: Element string following the Clark's Notation"""
        element = element.split('}')[-1]
        xpath_path = \
            '//xs:element[@name="{element}"]' + \
            '/xs:annotation/xs:documentation'.format(element=element)
        return xpath_path

    def get_documentation(self, element, namespace=None, schema_str=None):
        """**Helper method:** should return an schema specific documentation
        given an element parsing or getting the `Clark's Notation`_
        `{url:schema}Element` from the message error on validate method.

        :param str element: Element string following the Clark's Notation
        :param dict namespace: Element string following the Clark's Notation

        :returns: The documentation text if exists
        :rtype: unicode

        .. _`Clark's Notation`: http://effbot.org/zone/element-namespaces.htm
        """
        if namespace is None:
            namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        schema_root = etree.parse(StringIO(self.schema))
        document = schema_root.xpath(self.get_element_from_clark(element),
                                     namespaces=namespace)
        return document and document[0].text or ''
