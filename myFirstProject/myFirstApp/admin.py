from django.contrib import admin

from .models import NewsItem
from .models import Event

admin.site.register(NewsItem)
admin.site.register(Event)
