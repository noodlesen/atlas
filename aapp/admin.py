
"""Django admin config."""

from django.contrib import admin
from .models import Stock, Country
from .models import Industry, Sector, Metric, Bar
from aapp.evo_models import EvoReport, Portfolio, Capital
#from aapp.webfront_models import RawData

admin.site.register(Stock)
admin.site.register(Country)
admin.site.register(EvoReport)
admin.site.register(Industry)
admin.site.register(Sector)
admin.site.register(Portfolio)
admin.site.register(Capital)
#admin.site.register(RawData)
admin.site.register(Metric)
admin.site.register(Bar)
