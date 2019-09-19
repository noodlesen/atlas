
"""Run some command."""

from django.core.management.base import BaseCommand
from aapp.wf_simfin import load_bulk_data
from aapp.models import FundamentalEvent, Inst
from aapp.fabric.fabric import Fabric
from aapp.wf_simfin import load_bulk_data
from aapp.wf_finviz import fv_scan_details

class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        
        insts = Inst.objects.filter(history__contains="Alpha")
        print(len(insts))
        insts.delete()