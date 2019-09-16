
"""LOAD DATA FROM SCANNED TICKERS."""

from django.core.management.base import BaseCommand
from aapp.webfront import wf_get_screen
from aapp.fabric.fabric import Fabric
from aapp.models import Inst


class Command(BaseCommand):
    """A Django command."""

    def handle(self, *args, **options):
        """A Django command body."""

        CHANNEL = ['DIS', 'WFC', 'VZ', 'T', 'KO']
        TRENDY = ['BA', 'ADBE', 'CAT', 'INTC', 'AAPL']
        OTHER1 = ['AXP', 'C', 'CSCO', 'DIS']
        OTHER2 = ['EBAY', 'F', 'FB', 'GS', 'HD', 'HOG', 'HPQ', 'IBM', 'JNJ']
        NEW = [
            'FE', 'SCI', 'GTN', 'MSGN', 'USM', 'DISCA', 'OGE', 'AROW', 'EXPO', 'TLP',
            'MMT', 'LION', 'ATI', 'MYGN'
        ]
        # sym1 = 'INTC'
        # sym2 = 'MYGN'
        # f = Fabric()
        # f.load_data([sym1, sym2], 'ASTOCKS', 'DAILY')
        # f.trim()
        # f.set_range_from_last(250)
        # if f.check():
        #     print (f.compare(sym1, sym2))

        f = Fabric()
        insts = Inst.objects.all()
        all_tickers = [i.ticker for i in insts]
        # all_tickers.extend(CHANNEL)
        # all_tickers.extend(TRENDY)
        # all_tickers.extend(OTHER1)
        # all_tickers.extend(OTHER2)
        # all_tickers.extend(NEW)
        # all_tickers = list(set(all_tickers))
        # sr = wf_get_screen()
        f.load_data(all_tickers, 'ASTOCKS', 'DAILY')
        print(f.check())

        tl = f.extract_timecode()
        print(tl[0], tl[-1], len(tl))

        f.map_timecode()




        # insts = Inst.objects.all()
        # all_tickers = [i.ticker for i in insts][-20:]
        # #all_tickers = ['ADBE', 'AAPL', 'C', 'CAT']
        # f = Fabric()
        # f.load_data(all_tickers, 'ASTOCKS', 'DAILY')
        # f.cut_last(250)
        # #f.trim()
        # for a in f.as_list():
        #     print(a.symbol, a.count, len(a.data), a.dt_from, a.dt_to)
        # print(f.check())

