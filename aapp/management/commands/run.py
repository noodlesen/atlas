
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.models import Metric, Day, Bar, Stock



class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        ds = list(set([m.date for m in Metric.objects.filter(imprecise=True)]))
        print(len(ds))
        spy = Stock.objects.get(symbol='ADBE')
        for d in ds:
            try:
                b = Bar.objects.get(stock=spy, d=d)
            except Bar.DoesNotExist:
                print('NONE')
            else:
                print(d)