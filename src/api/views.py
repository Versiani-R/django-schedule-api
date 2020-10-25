from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

# TODO: Add a view to check which days and hours are already booked


def index(request):
    return render(request, 'api/index.html')


def api_index(request):
    return HttpResponse('Hello! You are at the /api/ index!')


# TODO: Implement a detail all ?
# TODO: Implement an id parameter ?
def api_detail(request, day=1, month=2, year=2000):
    return HttpResponse('Hello! This is the detail page!')


# TODO: Check if day, month and year are valid
# TODO: Check if the meeting is in the future
# TODO: Redirect if success
# TODO: Raise 404 if no scheduled meeting with this date found
def api_schedule(request):
    # Standard checks
    if ('date' and 'hours' and 'minutes') not in request.POST:
        # TODO: handle error
        pass

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
        # TODO: Handle error
        pass

    # Check if the meeting was scheduled to the past
    current_date = datetime.now()

    # TODO: Change to >
    if current_date > datetime_object:  # AKA, if it's in the past
        # TODO: Handle error
        print(current_date, datetime_object)
        print('Current_date is bigger than datetime_object')
        pass

    return HttpResponse(f'{day}/{month}/{year} {hours}:{minutes} {datetime_weekday}')
    # return render(request, 'api/schedule.html')


def api_schedule_success(request):
    pass
