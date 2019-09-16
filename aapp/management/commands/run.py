
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        load_bulk_data('fundamentals.csv')
