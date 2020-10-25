from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from datetime import datetime

from .models import ScheduledDate

# TODO: Add a view to check which days and hours are already booked
# TODO: Refactor the code ( there are functions that do way too much stuff )


def index(request):
    return render(request, 'api/index.html')


def api_index(request):
    return HttpResponse('Hello! You are at the /api/ index!')


# TODO: Implement a detail all ?
# TODO: Implement an id parameter ?
def api_detail(request, day=1, month=2, year=2000):
    return HttpResponse('Hello! This is the detail page!')


# TODO: Check if hour
# TODO: Redirect if success
def api_schedule(request):
    # Standard checks
    if ('date' and 'hours' and 'minutes') not in request.POST:
        return redirect('schedule_error', error_code=1)

    """
    Date is a html input, whose type is 'date'
    It looks like this: 10-25-2020 (mm-dd-yyyy)

    Day: 25
    Month: 10
    Year: 2020


    Hours: 18
    Minutes: 59
    """  # Stupid time-variables ...
    date = request.POST['date']
    [day, month, year] = [date.split('-')[-i] for i in range(1, 4)]
    hours = request.POST['hours']
    minutes = request.POST['minutes']

    # Check if the meeting was scheduled to a saturday/sunday
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # months[int(month) - 1] -> months is 0-based while month is not
    datetime_string = f'{months[int(month) - 1]} {day} {year} {hours}:{minutes}'

    # passing all the variables to a datetime object
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    # get the week day of the datetime_object date
    # monday = 0, tuesday = 1, ..., saturday = 5, sunday = 6
    datetime_weekday = datetime.weekday(datetime_object)
    if datetime_weekday >= 5:
        return redirect('schedule_error', error_code=2)

    # Check if the meeting was scheduled to the past
    current_date = datetime.now()

    if current_date > datetime_object:  # AKA, if it's in the past
        return redirect('schedule_error', error_code=3)

    # TODO: Check if schedule day and hour is available
    scheduled_dates = ScheduledDate.objects.all()

    sanitized_datetime_object = str(datetime_object).split(' ')

    # print(sanitized_datetime_object)

    for scheduled_date in scheduled_dates:
        sanitized_scheduled_date = str(scheduled_date).split(' ')

        # print(type(scheduled_date))
        # print(type(datetime_object))

        # Both sanitized dates have the same format: year-month-day
        # checking to see if they are in the same day, if so, check for the hour
        # if the hour is the same, check for the minutes, if the minutes are the same
        # it cannot be added, since there are already a meeting scheduled to that time
        if sanitized_scheduled_date[0] == sanitized_datetime_object[0]:
            sanitized_scheduled_time = str(scheduled_date).split(' ')[1].split('+')[0]

            # Cannot schedule a meeting, because there is a meeting already scheduled
            if sanitized_scheduled_time == sanitized_datetime_object[1]:
                return redirect('schedule_error', error_code=4)

    # TODO: Redirect
    # TODO: Revise the names of the variables
    # TODO: Avoid race-condition
    current_timezone = timezone.get_current_timezone()
    timezone_aware_date = current_timezone.localize(datetime_object)

    new_aware_scheduled_meeting = ScheduledDate(date=timezone_aware_date)
    new_aware_scheduled_meeting.save()

    print(new_aware_scheduled_meeting.id)

    return HttpResponse(f'{day}/{month}/{year} {hours}:{minutes} {datetime_weekday}')


def api_error(request, error_code):
    return render(request, 'api/schedule_error.html', {'error_code': error_code})