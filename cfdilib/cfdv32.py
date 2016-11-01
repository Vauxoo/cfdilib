# -*- coding: utf-8 -*-

from .cfdilib import BaseDocument
from .tools import tools


class CFDv32(BaseDocument):
    """Invoice document to comply with
    cfdi: v3.2 for Invoice Mexico Standards."""

    def __init__(self, dict_invoice, debug_mode=False):
        self.template_fname = 'cfdv32.xml'
        # We explicitly cached into s3 with the local test then ensure use
        # the s3 url to use our cache. remove the tools.s3_url if you want to
        # load first in the future
        self.xslt_fname = \
            tools.s3_url('http://s3.vauxoo.com/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')
        self.global_namespace = 'http://www.sat.gob.mx/sitio_internet/cfd'
        self.set_template(self.template_fname)
        super(CFDv32, self).__init__(dict_invoice, debug_mode=debug_mode)
        # This method must be called from the inherited
        #   __init__ always AFTER the super.

    def set_template(self, template_fname):
        self.template = super(CFDv32, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        self.schema = super(CFDv32, self).set_schema(schema_fname)

    def set_xslt(self):
        # TODO: Standarize the schema in this way also,
        #       we can not use different algorithms here
        self.xstl = super(CFDv32, self).set_xslt()


def get_invoice(dict_invoice, debug_mode=False):
    return CFDv32(dict_invoice, debug_mode=debug_mode)


class CFDICoA(BaseDocument):
    """CoA document
    cfdi: v1.1 for Accounting."""

    def __init__(self, dict_accounts, debug_mode=False):
        self.template_fname = 'cfdi11coa.xml'
        # We explicitly cached into s3 with the local test then ensure use
        # the s3 url to use our cache. remove the tools.s3_url if you want to
        # load first in the future
        self.xslt_fname = \
            tools.s3_url('http://s3.vauxoo.com/esquemas/ContabilidadE/1_1/CatalogoCuentas/CatalogoCuentas_1_1.xslt')
        self.global_namespace = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogosParaEsqContE'
        self.set_template(self.template_fname)
        super(CFDICoA, self).__init__(dict_accounts, debug_mode=debug_mode)

    def set_template(self, template_fname):
        self.template = super(CFDICoA, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        self.schema = super(CFDICoA, self).set_schema(schema_fname)

    def set_xslt(self):
        # TODO: Standarize the schema in this way also,
        #       we can not use different algorithms here
        self.xstl = super(CFDICoA, self).set_xslt()


def get_coa(dict_accounts, debug_mode=False):
    return CFDICoA(dict_accounts, debug_mode=debug_mode)
