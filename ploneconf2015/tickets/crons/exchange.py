""" Update exchange rate
"""
import contextlib
import urllib2
from decimal import Decimal
import xml.etree.cElementTree as ET
from zope.component import queryAdapter
from zope.component.hooks import getSite
from collective.cron import crontab
from ploneconf2015.tickets.interfaces import ITicket
from ploneconf2015.tickets.config import BNR

class UpdateExchangeRateJob(crontab.Runner):
    """ Update EUR to RON exchange rate
    """
    def run(self):
        """ Run cron
        """
        settings = queryAdapter(getSite(), ITicket)
        with contextlib.closing(urllib2.urlopen(BNR)) as conn:
            text = conn.read()
            tree = ET.fromstring(text)
            for rate in tree.iter():
                if rate.get('currency', None) == 'EUR':
                    value = Decimal(rate.text)
                    settings.exchange_rate = value
                    return "Exchange rate updated to: %s" % value
        return "Exchange rate didn't update!"
