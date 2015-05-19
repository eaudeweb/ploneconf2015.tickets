""" Tickets interfaces
"""
from zope import schema
from decimal import Decimal
from zope.interface import Interface
from ploneconf2015.tickets.config import PloneMessageFactory as _

class ITicket(Interface):
    """ Ticket settings
    """
    price = schema.Decimal(
        title=_(u"Price"),
        description=_(u"Plone Conference 2015 Ticket price in EUR"),
        default=Decimal('306.45')
    )

    vat = schema.Decimal(
        title=_(u"VAT"),
        description=_(u"V.A.T. in Romania. Ex. 24.0"),
        default=Decimal('24.0')
    )

    currency = schema.TextLine(
        title=_(u"Currency"),
        description=_(u"Currency should be EUR. Don't change it"),
        default=u'\u20ac'
    )

    exchange_rate = schema.Decimal(
        title=_(u"Exchange rate"),
        description=_(u"EUR to RON exchange rate"),
        default=Decimal('4.4')
    )

    early_birds = schema.Bool(
        title=_(u"Early birds"),
        description=_(u"Is the price above an 'Early birds' price?"),
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
