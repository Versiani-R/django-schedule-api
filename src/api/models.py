from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Command to  add new migrations: python manage.py makemigrations api
# Command to save new migrations: python manage.py migrate
class ScheduledDate(models.Model):
    """
    Hour: 8 to 18,
    Date: day/month/year
    """
    date = models.DateTimeField('scheduled meeting')
    count = models.IntegerField(default=1, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    objects = models.Manager()

    def __str__(self):
        return str(self.date)


class Name(models.Model):
    scheduled_date = models.ForeignKey(ScheduledDate, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
