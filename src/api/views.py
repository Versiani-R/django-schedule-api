from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

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

    return HttpResponse(f'{day}/{month}/{year} {hours}:{minutes} {datetime_weekday}')


def api_error(request, error_code):
    return render(request, 'api/schedule_error.html', {'error_code': error_code})