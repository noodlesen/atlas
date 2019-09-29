"""Webfront related ORM models."""
import json
import datetime

from django.db import models
from aapp.models import Stock
from webfront_models import RawData


class ApiCall(models.Model):
    """Every registered API call."""

    api = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(null=True)
    response = models.ForeignKey(RawData, on_delete=models.SET_NULL, null=True)


class RawData(models.Model):
    """Versatile class for any kind of raw data from requests."""

    created = models.DateTimeField(auto_now_add=True, null=True)
    query = models.TextField(null=True)
    data = models.TextField(null=True)
    data_type = models.CharField(max_length=20, null=True)
    author = models.CharField(max_length=20, null=True)


class FVDetails(models.Model):
    """FinViz stock details."""

    # No.    Ticker  Company Sector  Industry    Country Market Cap  P/E Fwd
    # P/E P/B Dividend    Recom   Price

    def __str__(self):
        """."""
        return('%s [%s]' % (self.company, self.ticker))

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    market_cap = models.FloatField(null=True)
    pe = models.FloatField(null=True)
    fwd_pe = models.FloatField(null=True)
    pb = models.FloatField(null=True)
    dividend = models.FloatField(null=True)
    recom = models.FloatField(null=True)
    price = models.FloatField(null=True)
    peg = models.FloatField(null=True)
    eps = models.FloatField(null=True)
    eps_this_year_growth = models.FloatField(null=True)
    eps_next_year = models.FloatField(null=True)
    eps_next_year_growth = models.FloatField(null=True)
    sales_past_5years_growth = models.FloatField(null=True)
    inst_own = models.FloatField(null=True)
    roa = models.FloatField(null=True)
    roe = models.FloatField(null=True)
    net_margin = models.FloatField(null=True)
    op_margin = models.FloatField(null=True)

    def parse(self, details):
        """Parse self-related screener results from it's own raw data."""
        idict = json.loads(details)

        self.company = idict['Company']

        if idict['Market Cap'] != '-':
            mc = float(idict['Market Cap'][:-1])
            mult = idict['Market Cap'][-1]
            if mult == 'M':
                mc *= 1000000
            elif mult == 'B':
                mc *= 1000000000
            self.market_cap = mc
        else:
            self.market_cap = None

        pes = idict['P/E']
        if pes == '-':
            pe = None
        else:
            pe = float(pes)
        self.pe = pe

        pbs = idict['P/B']
        if pbs == '-':
            pb = None
        else:
            pb = float(pbs)
        self.pb = pb

        pegs = idict['PEG']
        if pegs == '-':
            peg = None
        else:
            peg = float(pegs)
        self.peg = peg

        epss = idict['EPS (ttm)']
        if epss == '-':
            eps = None
        else:
            eps = float(epss)
        self.eps = eps

        eps_ny_g_s = idict.get('EPS next Y growth', '-')
        if eps_ny_g_s == '-':
            eps_ny_g = None
        else:
            eps_ny_g = float(eps_ny_g_s[:-1])
        self.eps_next_year_growth = eps_ny_g

        eps_ty_g_s = idict['EPS this Y']
        if eps_ty_g_s == '-':
            eps_ty_g = None
        else:
            eps_ty_g = float(eps_ty_g_s[:-1])
        self.eps_this_year_growth = eps_ty_g

        eps_ny_s = idict['EPS next Y']
        if eps_ny_s == '-':
            eps_ny = None
        else:
            eps_ny = float(eps_ny_s)
        self.eps_next_year = eps_ny

        sales_p5y_g_s = idict['Sales past 5Y']
        if sales_p5y_g_s == '-':
            sales_p5y_g = None
        else:
            sales_p5y_g = float(sales_p5y_g_s[:-1])
        self.sales_past_5years_growth = sales_p5y_g

        divs = idict['Dividend']
        if divs == '-':
            div = None
        else:
            div = float(divs[:-1])
        self.dividend = div

        roas = idict['ROA']
        if roas == '-':
            roa = None
        else:
            roa = float(roas[:-1])
        self.roa = roa

        roes = idict['ROE']
        if roes == '-':
            roe = None
        else:
            roe = float(roes[:-1])
        self.roe = roe

        inst_owns = idict['Inst Own']
        if inst_owns == '-':
            inst_own = None
        else:
            inst_own = float(inst_owns[:-1])
        self.inst_own = inst_own

        net_margins = idict['Profit Margin']
        if net_margins == '-':
            net_margin = None
        else:
            net_margin = float(net_margins[:-1])
        self.net_margin = net_margin

        op_margins = idict['Oper. Margin']
        if op_margins == '-':
            op_margin = None
        else:
            op_margin = float(op_margins[:-1])
        self.op_margin = op_margin

        recoms = idict['Recom']
        if recoms == '-':
            recom = None
        else:
            recom = float(recoms)
        self.recom = recom

        prs = idict['Price']
        if prs == '-':
            pr = None
        else:
            pr = float(idict['Price'])
        self.price = pr

        self.screen_scanned = True
        self.screen_last_updated = datetime.now()

        self.save()
