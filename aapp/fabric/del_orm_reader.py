"""DATA READING LIBRARY (USES DJANGO ORM)."""

import json
import datetime
from aapp.models import EvoReport, Stock


def save_report(name):
    """Save Evo report to DB."""
    r = EvoReport(name=name)
    r.save()


def load_settings_from_report(path):
    """Load Evo report from DB."""
    r = EvoReport.objects.get(name=path)
    print(r.name)
    return json.loads(r.raw_data)['input']



# REWRITE W BARS
def read_history_json(symbol):
    """Read history data from DB."""
    # stock = Stock.objects.get(symbol=symbol)
    # hdata = json.loads(inst.history)["Time Series (Daily)"]

    # src_data = [{key: hdata[key]} for key in sorted(hdata.keys())]

    # res_data = []
    # for d in src_data:
    #     dt = list(d.keys())[0]

    #     bar = {
    #         "open": float(d[dt]['1. open']),
    #         "high": float(d[dt]['2. high']),
    #         "low": float(d[dt]['3. low']),
    #         "datetime": datetime.datetime.strptime(dt, '%Y-%m-%d'),
    #         "close": float(d[dt]['4. close']),
    #         "volume": int(d[dt]['5. volume'])
    #     }

    #     res_data.append(bar)

    # return res_data

