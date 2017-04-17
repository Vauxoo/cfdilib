# -*- coding: utf-8 -*-

from .cfdilib import BaseDocument
from .tools import tools


class CFDv33(BaseDocument):
    """Invoice document to comply with
    cfdi: v3.3 for Invoice Mexico Standards."""

    def __init__(self, dict_invoice, debug_mode=False):
        self.template_fname = 'cfdv33.xml'
        # We explicitly cached into s3 with the local test then ensure use
        # the s3 url to use our cache. remove the tools.s3_url if you want to
        # load first in the future
        self.xslt_fname = tools.s3_url(
            'http://s3.vauxoo.com/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')
        self.global_namespace = 'http://www.sat.gob.mx/sitio_internet/cfd'
        self.set_template(self.template_fname)
        super(CFDv33, self).__init__(dict_invoice, debug_mode=debug_mode)
        # This method must be called from the inherited
        #   __init__ always AFTER the super.

    def set_template(self, template_fname):
        self.template = super(CFDv33, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        self.schema = super(CFDv33, self).set_schema(schema_fname)

    def set_xslt(self):
        # TODO: Standarize the schema in this way also,
        #       we can not use different algorithms here
        self.xstl = super(CFDv33, self).set_xslt()


def get_cfdi(dict_invoice, debug_mode=False):
    return CFDv33(dict_invoice, debug_mode=debug_mode)
