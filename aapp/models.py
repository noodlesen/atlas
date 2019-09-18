"""Atlas app Django models."""
import json

from datetime import datetime

from django.db import models


class Sector(models.Model):
    """A group of industries."""

    name = models.CharField(max_length=100)

    def __str__(self):
        """."""
        return(self.name)


class Industry(models.Model):
    """Exact industry."""

    name = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """."""
        return(self.name)


class Country(models.Model):
    """Country of an emmitent."""

    name = models.CharField(max_length=30)

    def __str__(self):
        """."""
        return(self.name)


class InstType(models.Model):
    """Type of an instrument."""

    TYPE_CHOICES = (('stock', 'Stock'),)
    name = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        """."""
        return(self.name)


class Inst(models.Model):
    """A trading instrument itself."""

    # No.    Ticker  Company Sector  Industry    Country Market Cap  P/E Fwd
    # P/E P/B Dividend    Recom   Price

    def __str__(self):
        """."""
        return('%s [%s]' % (self.company, self.ticker))

    company = models.CharField(max_length=100, null=True)
    ticker = models.CharField(max_length=10, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
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

    hist_last_update = models.DateTimeField(null=True)
    # screen_last_update = models.DateTimeField(null=True)
    details_last_update = models.DateTimeField(null=True)

    details = models.TextField(null=True)

    history = models.TextField(null=True)
    hist_from = models.DateField(null=True)
    hist_to = models.DateField(null=True)

    inst_type = models.ForeignKey(
        InstType, on_delete=models.CASCADE, null=True
    )

    def is_up_to_date(self):
        """Check if all the data is up to date."""
        res = False
        if self.hist_last_update and (
            self.hist_last_update - datetime.now()
        ).seconds < 24 * 3600:
            if self.details_last_update and (
                self.details_last_update - datetime.now()
            ).seconds < 24 * 3600:
                res = True
        return res

    def parse(self):
        """Parse self-related screener results from it's own raw data."""
        idict = json.loads(self.details)

        self.company = idict['Company']

        try:
            country = Country.objects.get(name=idict['Country'])
        except Country.DoesNotExist:
            country = Country(name=idict['Country'])
            country.save()

        try:
            sector = Sector.objects.get(name=idict['Sector'])
        except Sector.DoesNotExist:
            sector = Sector(name=idict['Sector'])
            sector.save()

        try:
            industry = Industry.objects.get(name=idict['Industry'])
        except Industry.DoesNotExist:
            industry = Industry(name=idict['Industry'])
            industry.sector = sector
            industry.save()

        self.country = country
        self.sector = sector
        self.industry = industry

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

        self.price = float(idict['Price'])

        self.screen_scanned = True
        self.screen_last_updated = datetime.now()

        # self.save()


class Capital(models.Model):
    """An independent amount of money used for simulation."""

    def __str__(self):
        """."""
        return '%s %d/%d' % (self.name, self.amount, self.balance)

    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    amount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True)


class Portfolio(models.Model):
    """An independent portfolio of instruments used for simulation."""

    def __str__(self):
        """."""
        return ('%s (%s)' % (self.name, self.capital.name))

    active = models.BooleanField(default=False)
    name = models.CharField(max_length=100, default=None)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    capital = models.ForeignKey(Capital, on_delete=models.CASCADE, null=True)


class Share(models.Model):
    """Instrument-to-Portfolio relation."""

    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=True
    )
    inst = models.ForeignKey(Inst, on_delete=models.CASCADE, null=True)


class EvoReport(models.Model):
    """A report produced by Evo."""

    name = models.CharField(max_length=100, default=None)
    raw_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """."""
        return(self.name)


class FabricStatus(models.Model):
    """Current status of Fabric (???)."""

    wip = models.BooleanField(default=False)
    task = models.CharField(max_length=20, null=True)

    def __str__(self):
        """."""
        if self.wip:
            return self.task
        else:
            return 'Idle'


class RawData(models.Model):
    """Versatile class for any kind of raw data."""

    created = models.DateTimeField(auto_now_add=True, null=True)
    query = models.TextField(null=True)
    data = models.TextField(null=True)
    data_type = models.CharField(max_length=20, null=True)
    author = models.CharField(max_length=20, null=True)


class FundamentalEvent(models.Model):
    """Fundamental news from companies."""
    def __str__(self):
        return ('%s %s %r %r' % (self.symbol, self.name, self.value, self.date))

    symbol = models.CharField(max_length=10, null=True)
    simfin_id = models.IntegerField(null=True)
    industry_code = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    value = models.FloatField(null=True)
    date = models.DateField(null=True)
