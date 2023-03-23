# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from .models import User

from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('id','username','tag')
    list_display_links=('id',)
    list_editable=('tag',)
    list_filter=('tag',)
    search_fields=('id',)
admin.site.register(User,UserAdmin)