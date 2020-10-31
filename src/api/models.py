from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ScheduledDate(models.Model):
    date = models.DateTimeField('scheduled meeting')
    count = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    objects = models.Manager()

    def __str__(self):
        return str(self.date)


class Information(models.Model):
    scheduled_date = models.ForeignKey(ScheduledDate, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    token_id = models.CharField(max_length=256)
    email = models.EmailField()

    def __str__(self):
        return self.name


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=256)
    token_id = models.CharField(max_length=256)
    api_calls = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.email


class Schedules(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField('scheduled meetings')

    def __str__(self):
        return str(self.date_and_time)
