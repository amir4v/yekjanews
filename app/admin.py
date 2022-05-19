from django.contrib import admin

from .models import Category, rssNews#, AparatVideo


#admin.site.register(AparatVideo)
admin.site.register(Category)
admin.site.register(rssNews)