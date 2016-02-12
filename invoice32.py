# -*- coding: utf-8 -*-

from cfdilib import BaseDocument

class Invoice32(BaseDocument):
    """An invoice object following 3.2 CFDI legal format.
    Due to avoid duplication of work we will delegate the error management
    Of attributes to the xsd, then the `validate` method will make the job of
    return the correct error, due to the standard managend on the invoice.

    The template itself must comply with an specific xsd, this is needed to
    simply pass a dictionary of terms used in the template convert them to
    attributes of this Invoice32 object using whatever attributes comes there

    Then due to the template itself has all the structure of attributes
    necessaries to comply with the xsd, theretically the xsd should return the
    logical error which we are not complying, see cfdv32.xml template to see
    how you should assembly a new version of this template, then set it to the
    template_fname attribute and guala your dict will be magically validated
    and converted to an XML file.

    Why not assembly with simple lxml?
    ----------------------------------

    Because it is more readable and configurable, it is always more simple
    inherit a class and set an attribute than overwrite hundreds of methods
    when it is a big xml.
    """

    def __init__(self, dict_invoice, debug_mode=False):
        """Convert a dictionary invoice to a Class

        @param :dict_invoice Dictionary with all entries you will need in your
        template.
        """
        self.debug_mode = debug_mode
        self.set_template_fname()
        self.set_schema_fname()
        self.set_template(self.template_fname)
        self.set_schema(self.schema_fname)
        self.__dict__.update(dict_invoice)
        for k, v in dict_invoice.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)
        self.set_cfd()

    def set_template_fname(self):
        """Wired to a known file which is a jinja2 valid template
        it works as an API."""
        self.template_fname = 'cfdv32.xml'

    def set_schema_fname(self):
        """The same than template but with .xsd on templates folder."""
        self.schema_fname = self.template_fname.replace('.xml', '.xsd')

    def set_template(self, template_fname):
        self.template = super(Invoice32, self).set_template(template_fname)

    def set_schema(self, schema_fname):
        self.schema = super(Invoice32, self).set_schema(schema_fname)

    def set_cfd(self):
        """cfd: xml just rendered already validated against xsd to be signed.

        :params boolean debug_mode: Either if you want the rendered template to be saved either it
        is valid or not with the given schema.

        :returns boolean: Either was valid or not the generated document.
        """
        cfd = self.template.render(inv=self)
        self.cfd = False
        if self.debug_mode:
            self.cfd = cfd
        if self.validate(self.schema, cfd):
            self.cfd = cfd


def get_invoice(dict_invoice, debug_mode=False):
    return Invoice32(dict_invoice, debug_mode=debug_mode)
