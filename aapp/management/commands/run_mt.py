
"""Multitester launcher."""

from django.core.management.base import BaseCommand
from aapp.fabric.fabric import Fabric
from aapp.fabric.multitester import multitest
import json
from aapp.models import Stock
from random import sample

par = """

{
    "input": {
        "FTP": 0.2351,
        "cci_f_per": 9,
        "cut_mix": 0.87,
        "cut_period": 2,
        "cut_treshold": 0.004,
        "dh_fast": 4,
        "dh_slow": 19,
        "fia_dmax": 26,
        "fia_dmin": 10,
        "fia_treshold": 0.11,
        "hf_max_per": 203,
        "hf_max_th": 0.93,
        "init_sl_k": 0.603,
        "max_pos": 100,
        "open_BREAK": false,
        "open_C2": true,
        "open_DOUBLE_HAMMER": true,
        "open_FRACTAL": false,
        "open_HAMMER": true,
        "open_TAIL": true,
        "ptbf_mix": 0.09,
        "ptc2_mix": 0.56,
        "ptdj_mix": 0.26,
        "pth_mix": 0.66,
        "ptss_mix": 0.44,
        "pttf_mix": 0.65,
        "rel_tp_k": 0.573,
        "sma_f_per_1": 7,
        "sma_f_per_2": 18,
        "sma_f_per_3": 41,
        "tp_koef": 1.5,
        "use_BREAKEVEN": false,
        "use_CCI_FILTER": true,
        "use_CUT": false,
        "use_FIA": false,
        "use_FTP": true,
        "use_HIGH_FILTER": false,
        "use_PTBF": false,
        "use_PTC2": false,
        "use_PTDJ": false,
        "use_PTH": false,
        "use_PTSS": false,
        "use_PTTF": false,
        "use_SMA_FILTER": false
    },
    "output": {
        "AVG_LOSS": 0,
        "AVG_WIN": 104.76016219725228,
        "CLOSE_REASONS": {
            "TP": [
                483,
                50679.93502443284
            ]
        },
        "DAYS_AVG": 408.06611570247935,
        "DAYS_MAX": 686,
        "DAYS_MIN": 204,
        "LOSES": 0,
        "MAX_DRAWDOWN": 47.140000000000015,
        "MAX_LOSES_IN_A_ROW": 0,
        "MAX_LOSS_PER_TRADE": 0,
        "MAX_PROFIT_PER_TRADE": 182.39468773584917,
        "MAX_WINS_IN_A_ROW": 484,
        "OPEN_REASONS": {
            "C2_BUY": [
                210,
                21880.472346580435
            ],
            "DOUBLE_HAMMER": [
                1,
                114.02163950381686
            ],
            "HAMMER_BUY": [
                19,
                1895.9080228649702
            ],
            "TAIL_BUY": [
                250,
                26552.484369685943
            ]
        },
        "PROFIT": 50703.91850347011,
        "ROI": 101.51888851909128,
        "TOTAL_INV": 49945.304999999986,
        "TRADES": 484,
        "VERS": 1.0,
        "WINRATE": 1.0,
        "WINS": 484,
        "WINS_TO_LOSES": null
    }
}
"""


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
        sel = ['KO']
        #stocks = Stock.objects.all()
        #sel = [s.symbol for s in sample(list(stocks), 20)]
        f = Fabric()
        f.load_data(sel, 'ASTOCKS', 'DAILY')
        f.map_timecode()
        #f.trim()
        #if f.check():
        f.set_range_from_last(4750)
        #params = load_settings_from_report('R101')
        params = json.loads(par)['input']
        print(params)
        print('!!!')
        r = multitest(f, params, draw=True, verbose=True)
        print(r)
