
"""Run some command."""

import datetime
from django.core.management.base import BaseCommand
from aapp.models import Day, Bar, Stock
from operator import itemgetter
from random import sample



class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""


        pl = 4

        patterns = {}

        symbols = ['AAPL', 'ADBE', 'KO', 'C', 'CAT', 'INTC', 'BA']
        #symbols = [st.symbol for st in Stock.objects.all()]
        for s in symbols:
            st = Stock.objects.get(symbol=s)
            dtf = datetime.date(2000, 1, 1)
            dtt = datetime.date(2017, 12, 31)
            days = [
                d.number
                for d in Day.objects.filter(date__gte=dtf, date__lte=dtt)
            ]
            bars = Bar.objects.filter(
                day__gte=min(days),
                day__lte=max(days),
                stock=st
            )
            bars = [b.as_candle() for b in bars]

            for i, d in enumerate(bars):
                if i >= pl - 1:
                    points = []
                    for sh in range(0, pl):
                        points.extend([
                            ('4' + str(sh), bars[i - sh].close_price),
                            ('3' + str(sh), bars[i - sh].low_price),
                            ('2' + str(sh), bars[i - sh].high_price),
                            ('1' + str(sh), bars[i - sh].open_price),
                        ])
                    points = sorted(points, key=itemgetter(1), reverse=True)
                    code = (''.join(p[0] for p in points))
                    if not patterns.get(code, False):
                        patterns[code] = 1
                    else:
                        patterns[code] += 1

        for p in sorted(patterns.items(), key=itemgetter(1), reverse=False):
            print(p)




