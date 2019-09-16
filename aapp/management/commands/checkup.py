
"""Checks if all the insrtuments are updated."""

# import json

from aapp.fabric.fabric import Asset

from aapp.models import Inst

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        insts = Inst.objects.all()
        for i in insts:
            # h = json.loads(i.history)
            print(i.ticker, i.is_up_to_date(), i.hist_from, i.hist_to)
            a = Asset()
            a.load_asset(i.ticker, 'ASTOCKS', 'DAILY')
