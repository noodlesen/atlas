from aapp.models import FundamentalEvent
from datetime import datetime

def load_bulk_data(fn):
    with open(fn, 'r') as f:
        lines = [l.split(';') for l in f.read().split('\n')][1:-1]
        lnum = len(lines)
        for i, l in enumerate(lines):
            print('%d/%d' % (i, lnum))
            e = FundamentalEvent()
            e.symbol = l[0]
            e.simfin_id = int(l[1])
            e.industry_code = int(l[2])
            e.name = l[3]
            e.date = datetime.strptime(l[4], '%Y-%m-%d')
            e.value = float(l[5])
            e.save()