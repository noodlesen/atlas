"""EVO related ORM models."""

from django.db import models
from aapp.models import Stock


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


class Pie(models.Model):
    """Instrument-to-Portfolio relation."""

    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=True
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)


class EvoReport(models.Model):
    """A report produced by Evo."""

    def __str__(self):
        """."""
        return(self.name)

    name = models.CharField(max_length=100, default=None)
    raw_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
