""" Custom options
"""
from eea.pdf.themes.pdfview import BodyOptionsMaker as PDFBody

class BodyOptionsMaker(PDFBody):
    """ Custom body
    """
    @property
    def body(self):
        """ Safely get pdf.body
        """
        body = super(BodyOptionsMaker, self).body
        request = getattr(self.context, 'REQUEST', {})
        p_sign = request.get('P_SIGN', "")
        return u"%s?P_SIGN=%s" % (body, p_sign)
