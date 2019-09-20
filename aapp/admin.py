
"""Django admin config."""

from django.contrib import admin
from .models import Inst, Country, EvoReport
from .models import Industry, Sector, Portfolio, Capital, RawData, FundamentalEvent

admin.site.register(Inst)
admin.site.register(Country)
admin.site.register(EvoReport)
admin.site.register(Industry)
admin.site.register(Sector)
admin.site.register(Portfolio)
admin.site.register(Capital)
admin.site.register(RawData)
admin.site.register(FundamentalEvent)
