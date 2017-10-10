# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Crisis, Call, Plan, SuggestedActions, Update

admin.site.register(Crisis)
admin.site.register(Call)
admin.site.register(Plan)
admin.site.register(SuggestedActions)
admin.site.register(Update)
