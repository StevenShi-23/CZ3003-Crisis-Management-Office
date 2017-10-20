# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Crisis, Call, Plan, SuggestedActions, Update
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


admin.site.register(Crisis)
admin.site.register(Call)
admin.site.register(Plan)
admin.site.register(SuggestedActions)
admin.site.register(Update)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)