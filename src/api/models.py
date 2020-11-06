from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    email = models.EmailField(default='No email provided.')
    password = models.CharField(max_length=256, default='No password provided.')
    token_id = models.CharField(max_length=256, default='No token id provided.')
    api_calls = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.email


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ''


class Register(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=256)

    objects = models.Manager()

    def __str__(self):
        return str(self.email)


class TimeList(models.Model):
    day = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    token_id = models.CharField(max_length=256)

    objects = models.Manager()

    def __str__(self):
        return '-'.join([self.day, self.month, self.year])


class ScheduleApi(models.Model):
    day = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    hours = models.CharField(max_length=2)
    minutes = models.CharField(max_length=2)
    company_name = models.CharField(max_length=200)
    token_id = models.CharField(max_length=256)

    objects = models.Manager()

    def __str__(self):
        return self.company_name
