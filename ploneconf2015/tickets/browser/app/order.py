""" Order view
"""
import json
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
    def date(self):
        """ Order date
        """
        date = self.context.creation_date
        return date.strftime('%d %b %Y')
