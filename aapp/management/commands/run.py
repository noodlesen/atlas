
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import Stock, Bar, Day
from aapp.fabric.fabric import Fabric
from aapp.wf_simfin import load_bulk_data
from aapp.wf_finviz import fv_scan_details
from datetime import datetime

class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        bars = Bar.objects.all()
        l = len(bars)
        for i, b in enumerate(bars):
            day = Day.objects.get(date=b.d)
            b.day = day.number
            b.save()
            print(i, l)

