
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import FundamentalEvent, Inst, Bar
from aapp.fabric.fabric import Fabric
from aapp.wf_simfin import load_bulk_data
from aapp.wf_finviz import fv_scan_details
from datetime import date
from aapp.fabric.orm_reader import read_history_json

class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        
        #Bar.objects.all().delete()
        syms = [i.ticker for i in Inst.objects.all()]
        l = len(syms)
        for i,s in enumerate(syms):
            print(s, i,'/',l )
            try:
                read_history_json(s, 'ASTOCKS', 'DAILY')
            except:
                print("Error reading", s)
                pass



