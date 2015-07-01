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
        data = json.loads(order.data)
        cart = data.get('cart', [])
        return order.vat_per_item * len(cart)

    def tva(self, order):
        """ Total VAT in RON
        """
        return order.exchange_rate * self.vat(order)

    def render(self, amount, currency=u''):
        """ Render money
        """
        amount = Decimal('%.2f' % amount)
        return u'%s%.2f' % (currency, amount)
