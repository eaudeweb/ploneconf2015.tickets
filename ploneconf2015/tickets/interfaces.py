""" Tickets interfaces
"""
from zope import schema
from zope.interface import Interface
from ploneconf2015.tickets.config import PloneMessageFactory as _

class ITicket(Interface):
    """ Ticket settings
    """
    price = schema.Float(
        title=_(u"Price"),
        default=275.0
    )

    vat = schema.Float(
        title=_(u"VAT"),
        default=24.0
    )

    currency = schema.TextLine(
        title=_(u"Currency"),
        default=u'\u20ac'
    )
