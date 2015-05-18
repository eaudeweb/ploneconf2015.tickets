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

    exchange_rate = schema.Float(
        title=_(u"Exchange rate"),
        default=4.5
    )

    early_birds = schema.Bool(
        title=_(u"Early birds"),
        default=True
    )

    merch_name = schema.TextLine(
        title=_(u"Merchant name"),
        default=u""
    )

    merch_url = schema.TextLine(
        title=_(u"Merchant URL"),
        default=u""
    )

    email = schema.TextLine(
        title=_(u"Email"),
        default=u""
    )

    key = schema.TextLine(
        title=_(u"Key"),
        default=u""
    )

    merchant = schema.TextLine(
        title=_(u"Merchant"),
        default=u""
    )

    terminal = schema.TextLine(
        title=_(u"Terminal"),
        default=u""
    )

    backref = schema.TextLine(
        title=_(u"Backref"),
        default=u""
    )

    postAction = schema.TextLine(
        title=_(u"Post action"),
        default=u""
    )

    submit = schema.TextLine(
        title=_(u"Submit"),
        default=u"trimite"
    )
