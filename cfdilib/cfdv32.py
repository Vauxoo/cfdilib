# -*- coding: utf-8 -*-

from .cfdilib import BaseDocument


class CFDv32(BaseDocument):
    """Invoice document to comply with
    cfdi: v3.2 for Invoice Mexico Standards."""

    def __init__(self, dict_invoice, debug_mode=False):
        self.template_fname = 'cfdv32.xml'
        self.xslt_fname = \
            'http://www.sat.gob.mx/sitio_internet/cfd/3/cadenaoriginal_3_2/cadenaoriginal_3_2.xslt'  # noqa
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
