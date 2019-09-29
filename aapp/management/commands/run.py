
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import Stock, Bar
from aapp.fabric.fabric import Fabric
from aapp.wf_simfin import load_bulk_data
from aapp.wf_finviz import fv_scan_details
from datetime import datetime

class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""

        symbols = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'JNJ']


        bars1 = []
        t1s = datetime.now()
        for s in symbols:
            bars1.extend([b.as_dict() for b in Bar.objects.filter(s=s)])
        t1f = datetime.now()


        bars2 = []
        t2s = datetime.now()
        for s in symbols:
            st = Stock.objects.get(symbol=s)
            bars2.extend([b.as_dict() for b in Bar.objects.filter(stock=st)])
        t2f = datetime.now()

        print(t1f-t1s, len(bars1))
        print(t2f-t2s, len(bars2))


