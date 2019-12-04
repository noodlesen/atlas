
"""Run some command."""

import datetime
from django.core.management.base import BaseCommand
from aapp.models import Day, Bar, Stock


class Trade():
    def __init__(self):
        self.active = False
        self.closed = False
        self.open_price = None
        self.open_date = None
        self.close_price = None
        self.close_date = None
        self.profit = None
        self.stock = None

    def open(self, b, **kwargs):
        at_open = kwargs.get('at_open', False)
        price = b.open_price if at_open else b.close_price
        if not self.active and not self.closed:
            self.active = True
            self.closed = False
            self.open_price = price
            self.open_date = b.datetime
            self.profit = 0
            self.stock = b.stock
            return True
        else:
            print('Error opening poition')
            return False

    def close(self,b,**kwargs):
        at_open = kwargs.get('at_open', False)
        price = b.open_price if at_open else b.close_price
        if self.active and not self.closed:
            self.active = False
            self.closed = True
            self.close_price = price
            self.close_date = b.datetime
            self.profit = self.close_price - self.open_price
            return True
        else:
            print('Error closing poition')
            return False




class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""

        st = Stock.objects.get(symbol='KO')
        dtf = datetime.date(2000, 1, 1)
        dtt = datetime.date(2017, 12, 31)
        days = [
            d.number for d in Day.objects.filter(date__gte=dtf, date__lte=dtt)
        ]
        bars = Bar.objects.filter(
            day__gte=min(days),
            day__lte=max(days),
            stock=st
        )
        bars = [b.as_candle() for b in bars]

        trades = []
        last_bar = None
        for i,d in enumerate(days):
            b = bars[i]
            if b.is_hammer():
                t = Trade()
                t.open(b)
                trades.append(t)
            if b.is_shooting_star():
                for t in trades:
                    if t.active:
                        t.close(b)
            last_bar = b

        for t in trades:
            if t.active:
                t.close(last_bar)

        total = 0
        for t in trades:
            print(t.profit)
            total+=t.profit
        print()
        print('PROFIT', total)