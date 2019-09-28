
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import FundamentalEvent, Inst, Bar
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

        syms = [i.ticker for i in Inst.objects.all()]
        l = len(syms)
        for i, s in enumerate(syms):
            print(s, i, '/', l)
            try:
                hh = read_history_json(s, 'ASTOCKS', 'DAILY')
                for h in hh:

                    bar = h
                    bar["symbol"] = s
                    bars.insert_one(bar)


            except:
                print("Error reading", s)
                pass

