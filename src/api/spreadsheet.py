"""
This whole file is dedicated to the creation of spreadsheets. It's existence is for marketing related
stuff. It does involve programming, but it's more related to marketing.

Note: This code is not accessible through normal runtime
"""

from datetime import date
from datetime import timedelta

from .models import User


def get_user(token_id):
    return User.objects.get(token_id=token_id)


# To get the token id of the user, just go to the admin page and search for it's email
def get_user_metrics(token_id):
    user = get_user(token_id)
    print(user.schedules_set.all())


# This function needs the date of the first day of the week to figure it out the week you actually want
def get_user_weekly_metrics(token_id, day, month, year):
    user = get_user(token_id)

    start_date = date(year, month, day)
    end_date = start_date + timedelta(days=7)

    print(user.schedules_set.filter(date_and_time__date__gte=start_date, date_and_time__date__lte=end_date))


def get_total_schedules_from_two_accounts(first_account_token_id, second_account_token_id):
    first_user = get_user(first_account_token_id)
    second_user = get_user(second_account_token_id)

    print(f'Total schedules of the first user:  \n{first_user.schedules_set.all()}')
    print(f'Total schedules of the second user: \n{second_user.schedules_set.all()}')
