"""
Pass for the admin:
1- +*+ 5
"""
from django.contrib import admin

from api.models import ScheduledDate, Information, User


class InformationInLine(admin.StackedInline):
    model = Information
    extra = 1


class ScheduledDateAdmin(admin.ModelAdmin):
    fields = ['date', 'count']
    inlines = [InformationInLine]


class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'password', 'token_id', 'api_calls']
    inlines = [InformationInLine]
    search_fields = ['email']


admin.site.register(ScheduledDate, ScheduledDateAdmin)
admin.site.register(User, UserAdmin)
