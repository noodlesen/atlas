
from pymongo import MongoClient
from operator import itemgetter
import json
from datetime import datetime
from time import sleep
import requests
from aapp.models import Bar, Industry, Sector, Stock, Metric, Day
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""

        client = MongoClient('mongodb://localhost:27017/')
        print(client)
        db = client.history_db

        BARS = db.bars
        INDUSTRIES = db.industries
        SECTORS = db.sectors
        METRICS = db.metrics
        STOCKS = db.stocks

        #Bar.objects.all().delete()

        # bars = list(BARS.find({}))
        # l = len(bars)
        # for i, b in enumerate(bars):
        #     print (i, l)
        #     new_bar = Bar(
        #         s=b['symbol'],
        #         o=b['open'],
        #         c=b['close'],
        #         h=b['high'],
        #         l=b['low'],
        #         v=b['volume'],
        #         d=b['datetime'].date()
        #     )
        #     new_bar.save()

        # scs = list(SECTORS.find({}))

        # #scs = list(set(scs))

        # inds = list(INDUSTRIES.find({}))

        # #inds = list(set(inds))

        # for sc in scs:
        #     s = Sector(
        #         name=sc['name']
        #     )
        #     s.save()

        # for ind in inds:
        #     try:
        #         Industry.objects.get(name=ind['name'])
        #     except Industry.DoesNotExist:
        #         i = Industry(
        #             name=ind['name']
        #         )
        #         s = Sector.objects.get(name=ind['sector'])
        #         i.sector = s
        #         i.save()
        #     else:
        #         print('ALREADY EXISTS')
        # Stock.objects.all().delete()
        # sts = list(STOCKS.find({}))



        # for st in sts:

        #     ind_name = st.get('industry', None)

        #     if ind_name is not None:

        #         try:
        #             ind = Industry.objects.get(name=ind_name)
        #         except Industry.DoesNotExist:
        #             ind = Industry(name=st['industry'], sector=None)
        #             ind.save()
        #     else:
        #         ind = None

        #     name = st.get('name', None)

        #     s = Stock(
        #         company=name,
        #         symbol=st['symbol'],
        #         industry=ind
        #     )
        #     s.save()

        # bars = Bar.objects.all()
        # bc = bars.count()
        # for i, b in enumerate(bars):
        #     b.stock = Stock.objects.get(symbol=b.s)
        #     b.save()
        #     print(int(i / bc * 100), '%')

        # ms = METRICS.find({})
        # for m in ms:
        #     print(m['symbol'], m['name'])
        #     st = Stock.objects.get(symbol=m['symbol'])
        #     mo = Metric(
        #         stock=st,
        #         date=m['date'].date(),
        #         name=m['name'],
        #         value=m['value'],
        #         simfin_id=m['simfin_id'],
        #         simfin_industry_code=m['industry_code']
        #     )
        #     mo.save()

        print(Metric.objects.all().count())


 
