
from pymongo import MongoClient
from operator import itemgetter
import json
from datetime import datetime
from time import sleep
import requests
from aapp.models import Bar
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

        bars = list(BARS.find({}))
        l = len(bars)
        for i, b in enumerate(bars):
            print (i, l)
            new_bar = Bar(
                s=b['symbol'],
                o=b['open'],
                c=b['close'],
                h=b['high'],
                l=b['low'],
                v=b['volume'],
                d=b['datetime'].date()
            )
            new_bar.save()
