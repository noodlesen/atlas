"""DATA READING LIBRARY (USES DJANGO ORM)."""

import json
import datetime
import aapp.sentinel as sentinel

from aapp.models import EvoReport, Inst


def save_report(name):
    """Save Evo report to DB."""
    r = EvoReport(name=name)
    r.save()


def load_settings_from_report(path):
    """Load Evo report from DB."""
    r = EvoReport.objects.get(name=path)
    print(r.name)
    return json.loads(r.raw_data)['input']


def read_history_json(symbol, itype, timeframe, **kwargs):
    """Read history data from DB."""
    adj = kwargs.get('adjusted', False)

    if itype == 'ASTOCKS':
        if timeframe == 'DAILY':
            dk = "Time Series (Daily)"
    elif itype == 'FX':
        if timeframe == 'DAILY':
            dk = "Time Series FX (Daily)"
        if timeframe == '60MIN':
            dk = "Time Series FX (60min)"

    if sentinel.check([symbol]):
        inst = Inst.objects.get(ticker=symbol)
        data = json.loads(inst.history)[dk]

        datalist = [{k: data[k]} for k in sorted(data.keys())]

        data = []
        for d in datalist:
            k = list(d.keys())[0]

            bar = {
                "open": float(d[k]['1. open']),
                "high": float(d[k]['2. high']),
                "low": float(d[k]['3. low']),
            }

            if timeframe in ['DAILY', 'WEEKLY', 'MONTHLY']:
                bar["datetime"] = datetime.datetime.strptime(k, '%Y-%m-%d')
            else:
                bar["datetime"] = datetime.datetime.strptime(
                    k, '%Y-%m-%d %H:%M:%S'
                )

            if itype == 'ASTOCKS':
                if adj:
                    bar["close"] = float(d[k]['5. adjusted close'])
                    bar["volume"] = int(d[k]['6. volume'])
                else:
                    bar["close"] = float(d[k]['4. close'])
                    bar["volume"] = int(d[k]['5. volume'])

            elif itype == 'FX':
                bar["close"] = float(d[k]['4. close'])
                bar["volume"] = 0

            if bar["datetime"].weekday() != 5:
                # исключаем субботы (для FX)
                data.append(bar)

        return data
