""" Orders listing
"""
import json
from decimal import Decimal
from Products.Five.browser import BrowserView


class OrdersListing(BrowserView):
    """ List orders
    """
    @property
    def orders(self):
        return self.context.getFolderContents(
            contentFilter={'portal_type':'order'},
            full_objects=True
        )

    def orderId(self, order):
        """ Get order id
        """
        return order.getId().replace('order-', '#')

    def orderBilling(self, order):
        """ Billing info
        """
        data = json.loads(order.data)
        return data.get('billing', {}).get('name', '')

    def vat(self, order):
        """ Total VAT
        """
        if getattr(order, 'discount', None):
            return 0
        data = json.loads(order.data)
        cart = data.get('cart', [])
        return order.vat_per_item * len(cart)

    def tva(self, order):
        """ Total VAT in RON
        """
        if getattr(order, 'discount', None):
            return 0
        return order.exchange_rate * self.vat(order)

    def price(self, order):
        """ Total price in EUR
        """
        if getattr(order, 'discount', None):
            return 0
        return order.price

    def pret(self, order):
        if getattr(order, 'discount', None):
            return 0
        return order.pret

    def render(self, amount, currency=u'', sign=u""):
        """ Render money
        """
        amount = Decimal('%.2f' % amount)
        return u'%s%s%.2f' % (sign, currency, amount)
