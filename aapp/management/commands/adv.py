
"""LOAD DATA FROM SCANNED TICKERS."""

from django.core.management.base import BaseCommand
from aapp.webfront import wf_get_screen
from aapp.fabric.fabric import Fabric
from aapp.models import Inst, FundamentalEvent


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""



        f = Fabric()

        events = FundamentalEvent.objects.all()

        print(len(events))
        all_tickers = list(set([e.symbol for e in events if e.symbol != '']))

        print(all_tickers)
        print(len(all_tickers))

        f.load_data(all_tickers, 'ASTOCKS', 'DAILY')
        print(f.check())

        tl = f.extract_timecode()
        print(tl[0], tl[-1], len(tl))

        f.map_timecode()


