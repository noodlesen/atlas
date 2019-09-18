
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import FundamentalEvent
from aapp.fabric.fabric import Fabric
from aapp.wf_simfin import load_bulk_data

class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        FundamentalEvent.objects.all().delete()
        load_bulk_data('fundamentals.csv')
