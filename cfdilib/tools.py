# -*- coding: utf-8 -*-
import urllib2
from tempfile import NamedTemporaryFile
from lxml import etree
import re
import time
from functools import wraps


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

    @staticmethod
    def is_url(element_name):
        return element_name.startswith('http')

    @staticmethod
    @retry(urllib2.URLError, tries=3, delay=3, back_off=2)
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
