""" Order content-type
"""
from zope.interface import implementer
from plone.dexterity.content import Container
from ploneconf2015.tickets.content.interfaces import IOrder

@implementer(IOrder)
class Order(Container):
    """ Order content-type
    """
