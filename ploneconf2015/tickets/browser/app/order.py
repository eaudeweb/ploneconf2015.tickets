""" Order view
"""
import json
from decimal import Decimal
from Products.Five.browser import BrowserView

class Order(BrowserView):
    """ Order view
    """
    def __init__(self, context, request):
        super(Order, self).__init__(context, request)
        self._data = None

    @property
    def data(self):
        """ Data
        """
        if self._data is None:
            self._data = json.loads(self.context.data )
        return self._data

    @property
    def oid(self):
        """ Order id
        """
        return self.context.getId().split('-')[1]

    @property
    def subtotal(self):
        """ Subtotal price
        """
        cart = self.data.get('cart', [])
        return self.context.price_per_item * len(cart)

    @property
    def vat(self):
        """ Total VAT
        """
        cart = self.data.get('cart', [])
        return self.context.vat_per_item * len(cart)

    @property
    def date(self):
        """ Order date
        """
        date = self.context.creation_date
        return date.strftime('%d %b %Y')

    def render(self, amount):
        """ Render money
        """
        amount = Decimal('%.2f' % amount)
        return u'\u20ac%.2f' % amount
