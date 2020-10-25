"""
Pass for the admin:
1- +*+ 5
"""


from django.contrib import admin

from .models import ScheduledDate


admin.site.register(ScheduledDate)
