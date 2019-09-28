
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import FundamentalEvent, Inst, Bar, Country
from aapp.fabric.fabric import Fabric
from aapp.wf_simfin import load_bulk_data
from aapp.wf_finviz import fv_scan_details
from datetime import date, datetime
from aapp.fabric.orm_reader import read_history_json
from pymongo import MongoClient


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        client = MongoClient('mongodb://localhost:27017/')
        print(client)
        db = client.history_db
        bars = db.bars

        dts = datetime(2007, 1, 1, 0, 0)
        dtf = datetime(2019, 9, 1, 0, 0)

        days = bars.distinct(
            'datetime',
            {
                'datetime': {'$gt': dts, '$lt': dtf}
            }
        )
        spy_days = bars.distinct(
            'datetime',
            {
                'symbol': 'SPY',
                'datetime': {'$gt': dts, '$lt': dtf}
            }
        )
        no_spy_days = [d for d in days if d not in spy_days]
        print(len(no_spy_days))

        lens = []
        for i, d in enumerate(no_spy_days):
            st = datetime.now()
            bb = bars.count_documents({'datetime': d})
            ft = datetime.now()
            result = ft - st
            v = (d, bb, result)
            lens.append(v)
            print(i,v, result)

        print (lens)

        # for i, d in enumerate(days):
        #     st = datetime.now()
        #     bb = list(bars.find({'datetime': d}))
        #     ft = datetime.now()
        #     result = ft - st
        #     print(result)
