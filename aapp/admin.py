
"""Django admin config."""

from django.contrib import admin
from .models import Stock, Country, EvoReport
from .models import Industry, Sector, Portfolio, Capital, RawData, Metric, Bar

admin.site.register(Stock)
admin.site.register(Country)
admin.site.register(EvoReport)
admin.site.register(Industry)
admin.site.register(Sector)
admin.site.register(Portfolio)
admin.site.register(Capital)
admin.site.register(RawData)
admin.site.register(Metric)
admin.site.register(Bar)
