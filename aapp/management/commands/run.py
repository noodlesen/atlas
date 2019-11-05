
"""Run some command."""

import datetime
from django.core.management.base import BaseCommand
from aapp.models import Day, Bar, Stock


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        st = Stock.objects.get(symbol='AAPL')
        dtf = datetime.date(2016, 1, 1)
        dtt = datetime.date(2017, 12, 31)
        days = [
            d.number for d in Day.objects.filter(date__gte=dtf, date__lte=dtt)
        ]
        bars = Bar.objects.filter(
            day__gte=min(days),
            day__lte=max(days),
            stock=st
        )
        for b in bars:
            print(b.d, b.c)
        # for d in days:
        #     print(d.date, Bar.objects.get(stock=st, day=d.number).c)
