""" Ticket form
"""
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from ploneconf2015.tickets.interfaces import ITicket

class Tickets(BrowserView):
    """ Tickers form controller
    """
    def __init__(self, context, request):
        super(Tickets, self).__init__(context, request)
        self._settings = None

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            self._settings = queryUtility(
                IRegistry).forInterface(ITicket, None)
        return self._settings

    @property
    def price(self):
        """
        :return: Ticket price
        """
        return getattr(self.settings, 'price', ITicket['price'].default)

    @property
    def vat(self):
        """
        :return: VAT
        """
        return getattr(self.settings, 'vat', ITicket['vat'].default)

    @property
    def currency(self):
        """
        :return: Currency
        """
        return getattr(self.settings, 'currency', ITicket['currency'].default)
