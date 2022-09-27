from django.contrib import admin

from . import models


# Register your models here.

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    list_display_links = ('key', 'value')


admin.site.register(models.Site, ConfigAdmin)
