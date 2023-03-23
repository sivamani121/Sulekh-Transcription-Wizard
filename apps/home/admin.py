# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Sentence,Answered
# Register your models here.
class SentenceAdmin(admin.ModelAdmin):
    list_display=('id','words','meaning','status')
    list_display_links=('words',)
    list_filter=('status',)
    search_fields=('words',)
admin.site.register(Sentence,SentenceAdmin)
class AnsweredAdmin(admin.ModelAdmin):
    list_display=('sentno','userid')
    list_display_links=('userid','sentno')
    
    
admin.site.register(Answered,AnsweredAdmin)