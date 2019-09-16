
"""Evo launcher."""

from django.core.management.base import BaseCommand

from aapp.fabric.evo2 import generate

from aapp.fabric.orm_reader import load_settings_from_report

from aapp.fabric.config import TS

from aapp.fabric.fabric import Fabric

USE_RANDOM = False

CHANNEL = ['DIS', 'WFC', 'VZ', 'T', 'KO']
TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
OTHER1 = ['AXP', 'C', 'CSCO', 'DIS']
OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'JNJ']
NEW = [
    'FE', 'SCI', 'GTN', 'MSGN', 'USM', 'DISCA', 'OGE', 'AROW', 'EXPO', 'TLP',
    'MMT', 'LION', 'ATI', 'MYGN'
]

GENERATIONS_COUNT = 20
MUTATIONS = 70
OUTSIDERS = 5
DEPTH = 10
STRATEGY = 'ROI_AND_WINRATE_AND_MINDD'
TIME_LIMIT = 570  # 5  # MINUTES


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""
        if USE_RANDOM:
            params = TS.get_random_ts_params()
        else:
            params = load_settings_from_report('R101')

        symbols = []
        symbols.extend(TRENDY)
        symbols.extend(CHANNEL)
        # symbols.extend(OTHER1)
        # symbols.extend(OTHER2)
        # symbols.extend(NEW)

        f = Fabric()
        f.load_data(symbols, 'ASTOCKS', 'DAILY')
        f.trim()
        f.set_range_from_last(500)
        if f.check():
            generate(
                f, GENERATIONS_COUNT, MUTATIONS, OUTSIDERS, DEPTH, STRATEGY,
                initial_params=params, report=True, time_limit=TIME_LIMIT
            )
