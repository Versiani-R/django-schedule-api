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


class Name(models.Model):
    scheduled_date = models.ForeignKey(ScheduledDate, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

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
