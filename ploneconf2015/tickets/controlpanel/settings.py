""" Control Panel
"""
from zope.component import queryUtility
from zope.interface import implements
from zope.formlib import form
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from plone.registry.interfaces import IRegistry
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from ploneconf2015.tickets.interfaces import ITicket
from ploneconf2015.tickets.config import PloneMessageFactory as _

class ControlPanel(ControlPanelForm):
    """ API
    """
    form_fields = form.FormFields(ITicket)

    label = _(u"Tickets Settings")
    description = _(u"Plone Conference tickets settings")
    form_name = _(u"Plone Conf. 2015 Tickets Settings")

class ControlPanelAdapter(SchemaAdapterBase):
    """ Form adapter
    """
    implements(ITicket)

    def __init__(self, context):
        super(ControlPanelAdapter, self).__init__(context)
        self._settings = None

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            self._settings = queryUtility(
                IRegistry).forInterface(ITicket, False)
        return self._settings

    @property
    def price(self):
        """ Get ticket price
        """
        name = u"price"
        return getattr(self.settings, name, ITicket[name].default)

    @price.setter
    def price(self, value):
        """ Set price
        """
        self.settings.price = value

    @property
    def vat(self):
        """ V.A.T.
        """
        name = u"vat"
        return getattr(self.settings, name, ITicket[name].default)

    @vat.setter
    def vat(self, value):
        """ Set V.A.T.
        """
        self.settings.vat = value

    @property
    def currency(self):
        """ Currency
        """
        name = u"currency"
        return getattr(self.settings, name, ITicket[name].default)

    @currency.setter
    def currency(self, value):
        """ Set currency
        """
        self.settings.currency = value

    @property
    def exchange_rate(self):
        """ Exchange rate
        """
        name = u"exchange_rate"
        return getattr(self.settings, name, ITicket[name].default)

    @exchange_rate.setter
    def exchange_rate(self, value):
        """ Set exchange rate
        """
        self.settings.exchange_rate = value

    @property
    def early_birds(self):
        """ Early birds
        """
        name = u"early_birds"
        return getattr(self.settings, name, ITicket[name].default)

    @early_birds.setter
    def early_birds(self, value):
        """ Set early_birds
        """
        self.settings.early_birds = value

    @property
    def merch_name(self):
        """ Metch name
        """
        name = u"merch_name"
        return getattr(self.settings, name, ITicket[name].default)

    @merch_name.setter
    def merch_name(self, value):
        """ Set merch_name
        """
        self.settings.merch_name = value

    @property
    def merch_url(self):
        """ Merch url
        """
        name = u"merch_url"
        return getattr(self.settings, name, ITicket[name].default)

    @merch_url.setter
    def merch_url(self, value):
        """ Set merch_url
        """
        self.settings.merch_url = value

    @property
    def email(self):
        """ Email
        """
        name = u"email"
        return getattr(self.settings, name, ITicket[name].default)

    @email.setter
    def email(self, value):
        """ Set email
        """
        self.settings.email = value

    @property
    def key(self):
        """ Key
        """
        name = u"key"
        return getattr(self.settings, name, ITicket[name].default)

    @key.setter
    def key(self, value):
        """ Set key
        """
        self.settings.key = value

    @property
    def merchant(self):
        """ merchant
        """
        name = u"merchant"
        return getattr(self.settings, name, ITicket[name].default)

    @merchant.setter
    def merchant(self, value):
        """ Set merchant
        """
        self.settings.merchant = value

    @property
    def terminal(self):
        """ terminal
        """
        name = u"terminal"
        return getattr(self.settings, name, ITicket[name].default)

    @terminal.setter
    def terminal(self, value):
        """ Set terminal
        """
        self.settings.terminal = value

    @property
    def backref(self):
        """ backref
        """
        name = u"backref"
        return getattr(self.settings, name, ITicket[name].default)

    @backref.setter
    def backref(self, value):
        """ Set backref
        """
        self.settings.backref = value

    @property
    def postAction(self):
        """ postAction
        """
        name = u"postAction"
        return getattr(self.settings, name, ITicket[name].default)

    @postAction.setter
    def postAction(self, value):
        """ Set postAction
        """
        self.settings.postAction = value

    @property
    def submit(self):
        """ submit
        """
        name = u"submit"
        return getattr(self.settings, name, ITicket[name].default)

    @submit.setter
    def submit(self, value):
        """ Set submit
        """
        self.settings.submit = value
