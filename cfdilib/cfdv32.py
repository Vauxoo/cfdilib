# -*- coding: utf-8 -*-

from cfdilib import BaseDocument


class CFDv32(BaseDocument):
    """Invoice document to comply with cfdi: v3.2 for Invoice Mexico Standards."""

    def __init__(self, dict_invoice, debug_mode=False):
        self.set_template_fname()
        self.set_template(self.template_fname)
        super(CFDv32, self).__init__(dict_invoice, debug_mode=debug_mode)
        # This method must be called from the inherited __init__ always AFTER the super.
        self.set_xml()

    def set_template_fname(self):
        """Wired to a known file which is a jinja2 valid template it works as an API then the
        file must be in template folder on library base path.
        """
        # TODO: Idea: may be it can be configurable in order to take the template from other
        # folder or even from the StringIO Itself.
        self.template_fname = 'cfdv32.xml'

    def set_template(self, template_fname):
        self.template = super(CFDv32, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        self.schema = super(CFDv32, self).set_schema(schema_fname)


def get_invoice(dict_invoice, debug_mode=False):
    return CFDv32(dict_invoice, debug_mode=debug_mode)
