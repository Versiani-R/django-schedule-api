from django.utils import timezone
from django.db import models

import datetime


# Command to  add new migrations: python manage.py makemigrations api
# Command to save new migrations: python manage.py migrate
class ScheduledDate(models.Model):
    """
    Hour: 8 to 18,
    Date: day/month/year
    """
    date = models.DateTimeField('scheduled meeting')

    def __str__(self):
        return str(self.date)

    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
