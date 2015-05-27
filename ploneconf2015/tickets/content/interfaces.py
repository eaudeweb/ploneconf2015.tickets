""" Content interfaces
"""
from zope import schema
from zope.interface import Interface
from plone.supermodel import model

class ITicketsStore(Interface):
    """ Marker interface for tickets store
    """

class IOrder(model.Schema):
    """ Order schema
    """
    data = schema.Text(
        title=u"Data",
        default=u"{}",
    )

    status = schema.Choice(
        title=u"Status",
        values=(u'pending', u'rejected', u'approved'),
        default=u'pending',
    )

    message = schema.TextLine(
        title=u"Message",
        description=u"Message from the bank",
        default=u""
    )

    p_sign = schema.TextLine(
        title=u"P Sign",
        description=u"Signature received from the bank",
        default=u""
    )

    early_birds = schema.Bool(
        title=u"Early Birds",
        description=u"Early birds tickets",
    )

    price = schema.Decimal(
        title=u"Price",
        description=u"Total price in EUR"
    )

    price_per_item = schema.Decimal(
        title=u"Price per item",
        description=u"Price per item in EUR"
    )

    vat_per_item = schema.Decimal(
        title=u"VAT per item",
        description=u"VAT per item in EUR"
    )

    pret = schema.Decimal(
        title=u"Pret",
        description=u"Total price in RON",
    )

    exchange_rate = schema.Decimal(
        title=u"Exchange rate"
    )
