from django.contrib import admin

from . import models


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_updated', 'registration_date', 'last_submitted')
    list_display_links = ('id', 'username', 'email')


admin.site.register(models.User, UserAdmin)
