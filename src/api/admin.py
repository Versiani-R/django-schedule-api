"""
Pass for the admin:
1- +*+ 5
"""
from django.contrib import admin

from .models import ScheduledDate, Name


class NameInLine(admin.StackedInline):
    model = Name
    extra = 1


class ScheduledDateAdmin(admin.ModelAdmin):
    fields = ['date', 'count']
    inlines = [NameInLine]


admin.site.register(ScheduledDate, ScheduledDateAdmin)
