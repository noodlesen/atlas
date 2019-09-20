"""DATA READING LIBRARY (USES DJANGO ORM)."""

import json
import datetime
import aapp.sentinel as sentinel

from aapp.models import EvoReport, Inst, Bar


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
    save_bar = kwargs.get('bar', False)

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
        hdata = json.loads(inst.history)[dk]

        src_data = [{key: hdata[key]} for key in sorted(hdata.keys())]

        res_data = []
        for d in src_data:
            dt = list(d.keys())[0]

            bar = {
                "open": float(d[dt]['1. open']),
                "high": float(d[dt]['2. high']),
                "low": float(d[dt]['3. low']),
            }

            if timeframe in ['DAILY', 'WEEKLY', 'MONTHLY']:
                bar["datetime"] = datetime.datetime.strptime(dt, '%Y-%m-%d')
            else:
                bar["datetime"] = datetime.datetime.strptime(
                    dt, '%Y-%m-%d %H:%M:%S'
                )

            if itype == 'ASTOCKS':
                if adj:
                    bar["close"] = float(d[dt]['5. adjusted close'])
                    bar["volume"] = int(d[dt]['6. volume'])
                else:
                    bar["close"] = float(d[dt]['4. close'])
                    bar["volume"] = int(d[dt]['5. volume'])

            elif itype == 'FX':
                bar["close"] = float(d[dt]['4. close'])
                bar["volume"] = 0

            if bar["datetime"].weekday() != 5:
                # исключаем субботы (для FX)
                res_data.append(bar)

            if save_bar:
                try:
                    Bar.objects.get(d=bar['datetime'].date(), s=symbol)
                except Bar.DoesNotExist:
                    b = Bar()
                    b.o = bar['open']
                    b.c = bar['close']
                    b.h = bar['high']
                    b.l = bar['low']
                    b.v = bar['volume']
                    b.d = bar['datetime'].date()
                    b.s = symbol
                    b.save()
                else:
                    print("BAR EXISTS")

        return res_data
