# -*- coding: utf-8 -*-
import logging
import re
import time
import urllib2

from tempfile import NamedTemporaryFile
from lxml import etree
from os.path import isfile
from functools import wraps

_logger = logging.getLogger(__name__)


def retry(exception_to_check, tries=4, delay=3, back_off=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exception_to_check: the exception to check. may be a tuple of
        exceptions to check
    :type exception_to_check: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param back_off: back_off multiplier e.g. value of 2 will double the
        delay each retry
    :type back_off: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e),
                                                             mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= back_off
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


class Tools(object):

    cached = {}

    @staticmethod
    def is_url(element_name):
        return element_name.startswith('http')

    @retry(urllib2.URLError, tries=3, delay=3, back_off=2)
    def cache_it(self, url):
        """Take an url which deliver a plain document  and convert it to a
        temporary file, this document is an xslt file expecting contains all
        xslt definitions, then the cache process is recursive.

        :param url: document origin url
        :return file path: local new absolute path
        """
        def cache_it(_url):
            cached = NamedTemporaryFile(delete=False)
            named = cached.name
            _response = urllib2.urlopen(_url)
            _content = _response.read()
            with cached as cache:
                cache.write(_content)
            self.cached.update({_url: named})
            return _content, named

        # If on this runtime it is cached do not cache it again.
        if self.cached.get(url) and isfile(self.cached[url]):
            return self.cached[url]

        internal = 0

        # TODO: unwire this to xslt, but usefull for know
        if url.endswith('xslt') and not internal:

            # Opening the first file just the first time.

            response = urllib2.urlopen(url)
            content = response.read()

            # Find all urls in the main xslt file.

            urls = re.findall(r'href=[\'"]?([^\'" >]+)', content)

            # Mapping all internal url in the file to local cached files.

            for u in urls:
                internal += 1
                content, _file = cache_it(u)
                content.replace(u, _file)
        return cache_it(url)[1]

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
