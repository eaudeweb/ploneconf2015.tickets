""" Ticket form
"""
import json
import logging
import base64
import binascii
import hmac
import hashlib
import phpserialize
from random import randint
from datetime import datetime
from zope.component import queryUtility, queryAdapter
from zope.component.hooks import getSite
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from ploneconf2015.tickets.interfaces import ITicket
logger = logging.getLogger('ploneconf2015.tickets')

class TicketsBuyForm(BrowserView):
    """ Tickers form controller
    """
    def __init__(self, context, request):
        super(TicketsBuyForm, self).__init__(context, request)
        self._settings = None

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            self._settings = queryAdapter(getSite(), ITicket)
        return self._settings

    def exchange(self, value):
        """ Exchange to RON
        """
        return value * 4.4

class TicketsCartForm(TicketsBuyForm):
    """ Cart
    """

    def getString(self, stype='preAuthPost', form={}, timestamp=''):
        """ Validation string
        """
        amount = form.get('AMOUNT')
        currency = form.get('CURRENCY')
        order = form.get('ORDER')
        desc = form.get('DESC')
        merch_name = self.settings.merch_name
        merch_url = self.settings.merch_url
        merchant = self.settings.merchant
        terminal = self.settings.terminal
        email = self.settings.email
        nonce = form.get('NONCE')
        backref = self.settings.backref

        if stype == 'preAuthPost':
            return "".join((
                "%s%s" % (len(amount), amount),
                "%s%s" % (len(currency), currency),
                "%s%s" % (len(order), order),
                "%s%s" % (len(desc), desc),
                "%s%s" % (len(merch_name), merch_name),
                "%s%s" % (len(merch_url), merch_url),
                "%s%s" % (len(merchant), merchant),
                "%s%s" % (len(terminal), terminal),
                "%s%s" % (len(email), email),
                "10",                                   # len(trtype), trtype
                "--",                                   # country, merch_gmt
                "%s%s" % (len(timestamp), timestamp),
                "%s%s" % (len(nonce), nonce),
                "%s%s" % (len(backref), backref)
            ))
        elif stype == "preAuthResponse":
            action = self.request.get('ACTION')
            rc = self.request.get('RC')
            message = self.request.get('MESSAGE')
            approval = self.request.get('APPROVAL')
            rrn = self.request.get('RRN')
            int_ref = self.request.get("INT_REF")

            if not approval.strip():
                txt_approval = '-'
            else:
                txt_approval = "%s%s" % (len(approval), approval)

            if not rrn.strip():
                txt_rrn = '-'
            else:
                txt_rrn = "%s%s" % (len(rrn), rrn)

            if not int_ref.strip():
                txt_int_ref = '-'
            else:
                txt_int_ref = "%s%s" % (len(int_ref), int_ref)


            return "".join((
                "%s%s" % (len(terminal), terminal),
                "10",                                    # len(trtype), trtype
                "%s%s" % (len(order), order),
                "%s%s" % (len(amount), amount),
                "%s%s" % (len(currency), currency),
                "%s%s" % (len(desc), desc),
                "%s%s" % (len(action), action),
                "%s%s" % (len(rc), rc),
                "%s%s" % (len(message), message),
                "%s%s" % (txt_rrn, txt_int_ref),
                "%s" % txt_approval,
                "%s%s" % (len(timestamp), timestamp),
                "%s%s" % (len(nonce), nonce),
            ))

    def getHexKey(self):
        """ Hex key

            php> $this->hex_key = pack('H*', $this->key);
        """
        return binascii.unhexlify(self.settings.key)

    def getPsign(self, form, timestamp):
        """ P Sign

            php> $this->psign = strtoupper(hash_hmac('sha1',
                                           $this->string, $this->hex_key));
        """
        data = form.get('STRING')
        key = self.getHexKey()
        return hmac.new(key, data, hashlib.sha1).hexdigest().upper()


    def getData(self, form, cart):
        """
        Get custom data
        """
        output = {
            'ProductsData': {},
            'UserData': {
                'Email': 'test@eaudeweb.ro',
                'Name': 'Test Xulescu',
                'Phone': '+40721345678',
                'BillingName': 'SC Test.RO SRL',
                'BillingEmail': 'contact@eaudeweb.ro',
                'BillingPhone': '+40212221522',
                'BillingCity': 'Roma',
                'BillingCountry': 'Iran',
            },
        }

        vat = 1 + self.settings.vat / 100.0
        for index, item in enumerate(cart):
            output['ProductsData'][index] = {
                "ItemName": "%s %s" % (item['firstName'], item['lastName']),
                "ItemDesc": item['email'],
                "Quantity": "1",
                "Price": "%.2f" % self.exchange( self.settings.price * vat )
            }

        output = phpserialize.dumps(output)
        return base64.b64encode(output)

    def checkout(self, cart):
        """ Checkout cart
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

        items = len(cart)
        vat = 1 + self.settings.vat / 100.0
        price = self.exchange(items * self.settings.price * vat)

        order = randint(100001, 999999)
        form = {
            'AMOUNT': "%.2f" % price,
            "CURRENCY": "RON",
            "ORDER": "%s" % order, #'100051',
            "DESC": "Tickets for order %s" % order,
            "TERMINAL": self.settings.terminal,
            "TIMESTAMP": timestamp,
            "NONCE": hashlib.md5(
                "shopperkey_%d" % randint(99999,9999999)).hexdigest(),
            "BACKREF": self.settings.backref,
        }

        form['DATA_CUSTOM'] = self.getData(form=form, cart=cart)
        form["STRING"] = self.getString(form=form, timestamp=timestamp)
        form["P_SIGN"] = self.getPsign(form=form, timestamp=timestamp)
        return json.dumps(form)

    def __call__(self, **kwargs):
        if self.request.method.lower() != 'post':
            return self.index()

        self.request.stdin.seek(0)
        data = self.request.stdin.read()

        cart = []
        try:
            data = json.loads(data)
            cart = data.get('cart', [])
        except Exception, err:
            logger.exception(err)
            raise

        if not cart:
            return json.dumps({})
        return self.checkout(cart)

class TicketsPurchasedForm(TicketsCartForm):
    """ Tickets purchased
    """
    def __init__(self, context, request):
        super(TicketsPurchasedForm, self).__init__(context, request)
        self._response = {}

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        """ Transaction message
        """
        return self.response.get("MESSAGE", "")

    @property
    def approved(self):
        """ Transaction approved?
        """
        if self.response.get('ACTION', None) != '0':
            return False
        if self.response.get('RC', None) != '00':
            return False
        return True

    def __call__(self, *args, **kwargs):
        self._response = self.request.form
        return self.index()
