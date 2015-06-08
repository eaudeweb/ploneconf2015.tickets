""" Ticket form
"""
import json
import logging
import base64
import binascii
import hmac
import hashlib
import phpserialize
from decimal import Decimal
from random import randint
from datetime import datetime
from zope.component import  queryAdapter, queryMultiAdapter
from zope.component.hooks import getSite
from zExceptions import BadRequest
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
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
        return Decimal(value * self.settings.exchange_rate
                       ).quantize(Decimal('.01'))

class TicketsCheckoutForm(TicketsBuyForm):
    """ Checkout
    """

    def getString(self, form={}, timestamp=''):
        """ Validation string
        """
        amount = form.get(u'AMOUNT')
        currency = form.get(u'CURRENCY')
        order = form.get(u'ORDER')
        desc = form.get(u'DESC')
        merch_name = self.settings.merch_name
        merch_url = self.settings.merch_url
        merchant = self.settings.merchant
        terminal = self.settings.terminal
        email = self.settings.email
        nonce = form.get(u'NONCE')
        backref = self.settings.backref

        return u"".join((
            u"%s%s" % (len(amount), amount),
            u"%s%s" % (len(currency), currency),
            u"%s%s" % (len(order), order),
            u"%s%s" % (len(desc), desc),
            u"%s%s" % (len(merch_name), merch_name),
            u"%s%s" % (len(merch_url), merch_url),
            u"%s%s" % (len(merchant), merchant),
            u"%s%s" % (len(terminal), terminal),
            u"%s%s" % (len(email), email),
            u"10",                                   # len(trtype), trtype
            u"--",                                   # country, merch_gmt
            u"%s%s" % (len(timestamp), timestamp),
            u"%s%s" % (len(nonce), nonce),
            u"%s%s" % (len(backref), backref)
        ))


    def getHexKey(self):
        """ Hex key

            php> $this->hex_key = pack('H*', $this->key);
        """
        return binascii.unhexlify(self.settings.key)

    def getPsign(self, form):
        """ P Sign

            php> $this->psign = strtoupper(hash_hmac('sha1',
                                           $this->string, $this->hex_key));
        """
        data = form.get(u"STRING")
        key = self.getHexKey()
        return hmac.new(key, data, hashlib.sha1).hexdigest().upper()


    def getData(self, form, data):
        """
        Get custom data
        """
        billing = data.get(u'billing')
        name = billing.get(u'billingName')
        email = billing.get(u'billingEmail')
        phone = billing.get(u'billingPhone')
        cart = data.get(u'cart', [])
        output = {
            u'ProductsData': {},
            u'UserData': {
                u'Email': email,
                u'Name': name,
                u'Phone': phone,
                u'BillingName': name,
                u'BillingEmail': email,
                u'BillingPhone': phone,
                u'BillingCity': billing.get(u'billingCity'),
                u'BillingCountry': billing.get(u'billingCountry'),
                u'BillingAddress': billing.get(u'billingAddress'),
                u'BillingPostalCode': billing.get(u'billingPostalCode'),
            },
        }

        vat = 1 + self.settings.vat / 100
        for index, item in enumerate(cart):
            name = u"%s %s" % (item[u'firstName'], item[u'lastName'])
            categ = (u"Early birds ticket" if self.settings.early_birds
                                           else u"Regular ticket")
            pid = u"early" if self.settings.early_birds else u"regular"

            output[u'ProductsData'][index] = {
                u"ItemName": u"Ticket %s" % name,
                u"ItemDesc": u"Plone Conf. 2015 ticket - %s" % name,
                u"Categ": categ,
                u"Quantity": u"1",
                u"Price": u"%s" % self.exchange(self.settings.price * vat),
                u"ProductId": pid
            }

        output = phpserialize.dumps(output)
        return base64.b64encode(output)

    def getOrderId(self, data, price, pret):
        """
        :return: order id
        """
        tool = getToolByName(self.context, u'portal_types')
        info = tool.getTypeInfo(u'order')

        now = datetime.now().strftime(u'%Y%m%d')
        for index in range(1, 1000000):
            oid = u"%s%.2d" % (now, index)
            title = u"Tickets for order %s" % oid
            try:
                ob = info._constructInstance(
                    self.context, u'order-%s' % oid, title=title)
            except Exception:
                continue
            else:
                ob.exclude_from_nav = True
                ob.data = json.dumps(data)
                ob.early_birds = self.settings.early_birds
                ob.exchange_rate = self.settings.exchange_rate
                ob.price = price
                ob.price_per_item = self.settings.price.quantize(Decimal('.01'))
                ob.vat_per_item =  (self.settings.price * self.settings.vat/100
                                    ).quantize(Decimal('.01'))
                ob.pret = pret
                return oid
        raise EnvironmentError("Too many orders for today. Try tomorrow")

    def checkout(self, data):
        """ Checkout cart
        """
        cart = data.get(u'cart', [])
        timestamp = datetime.utcnow().strftime(u'%Y%m%d%H%M%S')

        items = len(cart)
        vat = 1 + self.settings.vat / 100
        price = items * (self.settings.price * vat).quantize(Decimal('.01'))
        pret_per_item = self.exchange(self.settings.price * vat)
        pret = items * pret_per_item

        order = self.getOrderId(data, price=price, pret=pret)
        title = u"Tickets for order %s" % order
        form = {
            u'AMOUNT': u"%s" % pret,
            u"CURRENCY": u"RON",
            u"ORDER": order,
            u"DESC": title,
            u"TERMINAL": self.settings.terminal,
            u"TIMESTAMP": timestamp,
            u"NONCE": hashlib.md5(
                u"shopperkey_%d" % randint(99999,9999999)).hexdigest(),
            u"BACKREF": self.settings.backref,
        }

        form[u'DATA_CUSTOM'] = self.getData(form=form, data=data)
        form[u"STRING"] = self.getString(form=form, timestamp=timestamp)
        form[u"P_SIGN"] = self.getPsign(form=form)

        return json.dumps(form)

    def __call__(self, **kwargs):
        if self.request.method.lower() != u'post':
            return self.request.response.redirect(
                self.context.absolute_url() + u'/tickets.buy')

        self.request.stdin.seek(0)
        data = self.request.stdin.read()
        form = {}
        try:
            form = json.loads(data)
        except Exception, err:
            logger.exception(err)

        if not form:
            return json.dumps({})
        return self.checkout(form)

class TicketsPurchasedForm(TicketsCheckoutForm):
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
        return self.response.get(u"MESSAGE", u"")

    @property
    def approved(self):
        """ Transaction approved?
        """
        if self.response.get(u'ACTION', None) != u'0':
            return False
        if self.response.get(u'RC', None) != u'00':
            return False
        return True

    @property
    def order(self):
        """ Return order id
        """
        return self.response.get(u'ORDER', u"")

    def getString(self, **kwargs):
        """ Validation string
        """
        terminal = self.response.get(u'TERMINAL', u"")
        trtype = self.response.get(u'TRTYPE', u"")
        order = self.response.get(u'ORDER', u"")
        amount = self.response.get(u'AMOUNT', u"")
        currency = self.response.get(u'CURRENCY', u"")
        desc = self.response.get(u'DESC', u"")
        rrn = self.response.get(u'RRN', u"")
        int_ref = self.response.get(u'INT_REF', u"")
        approval = self.response.get(u'APPROVAL' ,u"")
        nonce = self.response.get(u'NONCE', u"")
        action = self.response.get(u'ACTION', u"")
        message = self.response.get(u'MESSAGE', u"")
        rc = self.response.get(u'RC', u"")
        timestamp = self.response.get(u'TIMESTAMP', u"")

        if not approval.strip():
            txt_approval = '-'
        else:
            txt_approval = u"%s%s" % (len(approval), approval)

        if not rrn.strip():
            txt_rrn = u"-"
        else:
            txt_rrn = u"%s%s" % (len(rrn), rrn)

        if not int_ref.strip():
            txt_int_ref = u"-"
        else:
            txt_int_ref = u"%s%s" % (len(int_ref), int_ref)

        return u"".join((
            u"%s%s" % (len(terminal), terminal),
            u"%s%s" % (len(trtype), trtype),
            u"%s%s" % (len(order), order),
            u"%s%s" % (len(amount), amount),
            u"%s%s" % (len(currency), currency),
            u"%s%s" % (len(desc), desc),
            u"%s%s" % (len(action), action),
            u"%s%s" % (len(rc), rc),
            u"%s%s" % (len(message), message),
            u"%s%s" % (txt_rrn, txt_int_ref),
            u"%s" % txt_approval,
            u"%s%s" % (len(timestamp), timestamp),
            u"%s%s" % (len(nonce), nonce),
        ))

    def _approve(self, p_sign):
        """ Approve order
        """
        oid = u'order-%s' % self.response.get(u'ORDER', u'')
        try:
            ob = self.context[oid]
        except Exception, err:
            logger.exception(err)
            return

        email = json.loads(ob.data)['billing']['email']
        if ob.status == u'pending':
            ob.p_sign = p_sign
            ob.message = self.message
            ob.status = u'approved'
            download = queryMultiAdapter(
                (ob, self.request), name='download.pdf')
            download.download(email=email)

    def _reject(self, p_sign):
        """ Reject order
        """
        oid = u'order-%s' % self.response.get(u'ORDER', u'')
        try:
            ob = self.context[oid]
        except Exception, err:
            logger.exception(err)
            return

        if ob.status == u'pending':
            ob.p_sign = p_sign
            ob.message = self.message
            ob.status = u'rejected'

    def __call__(self, *args, **kwargs):
        self._response = self.request.form
        form = {u'STRING': self.getString()}
        p_sign = self.response.get(u'P_SIGN')
        my_p_sign = self.getPsign(form=form)
        if p_sign != my_p_sign:
            raise BadRequest(
                u'Invalid response from the bank! %s' % self.response)

        if self.approved:
            self._approve(p_sign)
        else:
            self._reject(p_sign)

        return self.index()

class TicketsPurchasedIPN(TicketsPurchasedForm):
    """ IPN
    """
    def __call__(self, *args, **kwargs):

        self._response = self.request.form
        logger.info(u"IPN call for order id %s", self.order)

        form = {u'STRING': self.getString()}
        p_sign = self.response.get(u'P_SIGN')
        my_p_sign = self.getPsign(form=form)
        if p_sign != my_p_sign:
            logger.exception(u'Invalid response from the bank! %s',
                             self.response)
            return u"0"

        if self.approved:
            self._approve(p_sign)
        else:
            self._reject(p_sign)

        return u"1"
