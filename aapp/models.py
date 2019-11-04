"""Atlas app Django models."""

from django.db import models


class Day(models.Model):
    """A trading day."""

    number = models.IntegerField(null=True)
    date = models.DateField(null=True)


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


class Stock(models.Model):
    """A trading instrument itself."""

    def __str__(self):
        """."""
        return('%s [%s]' % (self.company, self.symbol))

    company = models.CharField(max_length=100, null=True)
    symbol = models.CharField(max_length=10, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True)


class Metric(models.Model):
    """Fundamental news from companies."""

    def __str__(self):
        """."""
        return (
            '%s %s %r %r' % (
                self.stock.symbol, self.name, self.value, self.date
            )
        )

    # symbol = models.CharField(max_length=10, null=True)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    simfin_id = models.IntegerField(null=True)
    simfin_industry_code = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    value = models.FloatField(null=True)
    date = models.DateField(null=True)
    day = models.IntegerField(null=True)
    imprecise = models.BooleanField(default=False)


class Bar(models.Model):
    """Single day price bar."""

    def as_dict(self):
        """Price data as a dict."""
        return ({
            "open": self.o,
            "close": self.c,
            "high": self.h,
            "low": self.l,
            "volume": self.v,
            "datetime": self.d
        })

    o = models.FloatField(null=True)
    c = models.FloatField(null=True)
    h = models.FloatField(null=True)
    l = models.FloatField(null=True)
    v = models.IntegerField(null=True)
    d = models.DateField(null=True)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    # day = models.ForeignKey(Day, on_delete=models.SET_NULL, null=True)
    day = models.IntegerField(null=True)
