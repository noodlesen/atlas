# 1. Review portfolio. If not exists - create
# 2. check fundamentals for each. If not good - sell
# 3. check money, if remains look for new stocks
# 4. scan screener
# 5. select candidates
# 6. check correlation with portfolio and SPY
# 7. get sector fundamentals
# 8. choose new by sector and lowest correlation
# 9. buy

from aapp.models import Capital, Portfolio, Inst
from datetime import datetime
from aapp.scan_screen import Screen

from time import sleep
from random import randint
from aapp.fabric.fabric import Fabric


class Advisor():

    def __init__(self):

        try:
            cap = Capital.objects.get(name='test1')
        except Capital.DoesNotExist:
            cap = Capital(name='test1', amount=50000, balance=50000, start_date=datetime.today())
            cap.save()

        try:
            port = Portfolio.objects.get(name='test1_growth')
        except Portfolio.DoesNotExist:
            port = Portfolio(name='test1_growth', capital=cap, active=True)
            port.save()

    def find_new(self):
        s = Screen()
        sres = s.scan()
        tickers = [r['Ticker'] for r in sres]
        print (tickers)
        f = Fabric()
        f.load_data(tickers, 'ASTOCKS', 'DAILY')
        f.trim()
        if f.check():
            print ('FABRIC OK!')
