"""
Pass for the admin:
1- +*+ 5
"""
from django.contrib import admin

from .models import ScheduledDate, Information, User, Schedules


class InformationInLine(admin.StackedInline):
    model = Information
    extra = 1


class ScheduledDateAdmin(admin.ModelAdmin):
    fields = ['date', 'count']
    inlines = [InformationInLine]


class UserPastSchedulesInLine(admin.StackedInline):
    model = Schedules
    extra = 1


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'token_id', 'api_calls']
    inlines = [UserPastSchedulesInLine]
    search_fields = ['email']


admin.site.register(ScheduledDate, ScheduledDateAdmin)
admin.site.register(User, UserAdmin)
