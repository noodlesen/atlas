
"""Multitester launcher."""

from django.core.management.base import BaseCommand
from aapp.fabric.fabric import Fabric
from aapp.fabric.multitester import multitest
from aapp.fabric.orm_reader import load_settings_from_report


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        # symbols = [
        #     'FE', 'SCI', 'GTN', 'MSGN', 'USM', 'DISCA',
        #     'OGE', 'AROW', 'EXPO', 'TLP', 'MMT', 'LION',
        #     'ATI', 'MYGN'
        # ]
        # symbols = [
        #     'DIS', 'WFC', 'VZ', 'T', 'KO', 'BA', 'ADBE',
        #     'CAT', 'INTC', 'AAPL', 'AXP', 'C', 'CSCO',
        #     'DIS', 'EBAY', 'F', 'FB', 'GS', 'HD', 'HOG',
        #     'HPQ', 'IBM', 'ITX', 'JNJ', 'FE', 'SCI',
        #     'GTN', 'MSGN', 'USM', 'DISCA', 'OGE', 'AROW',
        #     'EXPO', 'TLP', 'MMT', 'LION', 'ATI', 'MYGN'
        # ]
        # symbols = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
        symbols = ["AAPL"]
        f = Fabric()
        f.load_data(symbols, 'ASTOCKS', 'DAILY')
        f.trim()
        if f.check():
            f.set_range_from_last(500)
            params = load_settings_from_report('atest')
            print(params)
            r = multitest(f, params, draw=True, verbose=True)
            print(r)
