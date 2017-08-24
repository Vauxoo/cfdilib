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


class Payroll12(BaseDocument):
    """Invoice document to comply with
    cfdi: v3.3 for Invoice Mexico Standards."""

    def __init__(self, dict_invoice, debug_mode=False):
        self.template_fname = 'payroll12.xml'
        # We explicitly cached into s3 with the local test then ensure use
        # the s3 url to use our cache. remove the tools.s3_url if you want to
        # load first in the future
        # TODO - Change by reference to payroll v1.2
        self.xslt_fname = tools.s3_url(
            'http://s3.vauxoo.com/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')
        self.global_namespace = 'http://www.sat.gob.mx/sitio_internet/cfd'
        self.set_template(self.template_fname)
        super(Payroll12, self).__init__(dict_invoice, debug_mode=debug_mode)
        # This method must be called from the inherited
        #   __init__ always AFTER the super.

    def set_template(self, template_fname):
        self.template = super(Payroll12, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        schema_fname = 'cfdv33.xsd'
        self.schema = super(Payroll12, self).set_schema(schema_fname)

    def set_xslt(self):
        # TODO: Standarize the schema in this way also,
        #       we can not use different algorithms here
        self.xstl = super(Payroll12, self).set_xslt()


def get_payroll(dict_payroll, debug_mode=False):
    return Payroll12(dict_payroll, debug_mode=debug_mode)


class Payment10(BaseDocument):
    """Invoice document to comply with
    cfdi: v3.3 for Invoice Mexico Standards. Complement to payments version 1.0
    """

    def __init__(self, dict_invoice, debug_mode=False):
        self.template_fname = 'payment10.xml'
        # We explicitly cached into s3 with the local test then ensure use
        # the s3 url to use our cache. remove the tools.s3_url if you want to
        # load first in the future
        # TODO - Change by reference to payroll v1.2
        self.xslt_fname = tools.s3_url(
            'http://s3.vauxoo.com/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt')
        self.global_namespace = 'http://www.sat.gob.mx/sitio_internet/cfd'
        self.set_template(self.template_fname)
        super(Payment10, self).__init__(dict_invoice, debug_mode=debug_mode)
        # This method must be called from the inherited
        #   __init__ always AFTER the super.

    def set_template(self, template_fname):
        self.template = super(Payment10, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        schema_fname = 'cfdv33.xsd'
        self.schema = super(Payment10, self).set_schema(schema_fname)

    def set_xslt(self):
        # TODO: Standarize the schema in this way also,
        #       we can not use different algorithms here
        self.xstl = super(Payment10, self).set_xslt()


def get_payment10(dict_payment, debug_mode=False):
    return Payment10(dict_payment, debug_mode=debug_mode)
