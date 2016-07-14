# -*- coding: utf-8 -*-
import urllib2
from tempfile import NamedTemporaryFile
from lxml import etree
import re


class Tools(object):

    @staticmethod
    def is_url(element_name):
        return element_name.startswith('http')

    @staticmethod
    def cache_it(url):
        """Take an url which deliver a plain document
        and convert it to a temporary file
        :param url: document origin url
        :return: local new absolute path
        """
        def cache_it(url):
            cached = NamedTemporaryFile(delete=False)
            named = cached.name
            with cached as cache:
                cache.write(content)
            return named
        response = urllib2.urlopen(url)
        content = response.read()
        internal = 0
        if url.endswith('xslt'):
            # TODO: unwire this to xslt, but usefull for know
            # to cache only the xslt which is the know one.
            urls = re.findall(r'href=[\'"]?([^\'" >]+)', content)
            if not internal:
                for u in urls:
                    internal += 1
                    _file = cache_it(u)
                    content.replace(u, _file)
        return cache_it(url)

    @staticmethod
    def get_original(document, xslt):
        """Get the original chain given document path and xslt local path

        :param str document: local absolute path to document
        :param str xslt: local absolute path to xst file
        :return: new chain generated.
        :rtype: str
        """
        dom = etree.parse(document)  # TODO: cuando este probando -
        # fuente:
        # http://stackoverflow.com/questions/16698935/how-to-transform-an-xml-file-using-xslt-in-python
        xslt = etree.parse(xslt)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        return newdom

tools = Tools()
