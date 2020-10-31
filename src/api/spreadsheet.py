"""
This whole file is dedicated to the creation of spreadsheets. It's existence is for marketing related
stuff. It does involve programming, but it's more related to marketing.

Note: This code is not accessible through normal runtime
"""

from datetime import date, timedelta, datetime

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


# This function gets the average of the newest and oldest schedule, so it's not as precise as a monthly average.
def get_user_entire_average_schedule_by_day(token_id):
    user = get_user(token_id)
    dates = user.schedules_set.all().order_by('date_and_time')

    if dates.count() < 2:
        print('Not enough schedules to create a metric')
        return

    newest_date = dates.first().date_and_time
    oldest_date = dates.last().date_and_time

    time_difference = oldest_date - newest_date

    print(f'Newest date: {newest_date}')
    print(f'Oldest date: {oldest_date}')
    print(f'Time difference: {time_difference}')
    print(f'Are they equal ? {newest_date == oldest_date}')

    if abs(time_difference.days) <= 0:
        print('The first and last date are the same. Cannot divide by zero.')
        return

    average = dates.count() / abs(time_difference.days)

    print(f'Average is: {average}')


# This function gets the average of the newest and oldest schedule of the month
def get_user_monthly_average_schedule_by_day(token_id, year, month):
    user = get_user(token_id)

    start_date = date(year, month, 1)
    end_date = start_date + timedelta(days=30)

    dates = user.schedules_set.filter(
        date_and_time__date__gte=start_date,
        date_and_time__date__lte=end_date
    )

    average = dates.count() / 30

    print(f'Average is: {average}')

