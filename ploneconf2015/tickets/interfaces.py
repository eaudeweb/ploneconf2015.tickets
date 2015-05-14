""" Tickets interfaces
"""
from ploneconf2015.tickets.controlpanel.interfaces import ITicket
from ploneconf2015.tickets.content.interfaces import ITicketsStore

__all__ = [
    ITicket.__name__,
    ITicketsStore.__name__,
]
