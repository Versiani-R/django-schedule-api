from django.db.models import ObjectDoesNotExist, F

from datetime import datetime

from .models import User, ScheduledDate
from .exceptions import InvalidPost, InvalidTokenId, InvalidApiCall


def is_date_valid(day, month, year):
    if len(day) != 2 or len(month) != 2:
        raise InvalidPost(message='Day and Month must be standardized! Read the "Data" at the official documentation.',
                          code=2)
    if len(year) != 4:
        raise InvalidPost(message='Year must be standardized! Read the "Data" at the official documentation.', code=2)

    if (int(day) < 1 or int(day) > 31) or (int(month) < 1 or int(month) > 12):
        raise InvalidPost(message='Day or Month value is incorrect! Read the "Data" at the official documentation.',
                          code=2)

    return True


def is_time_valid(hours, minutes):
    if len(hours) != 2 or len(minutes) != 2:
        raise InvalidPost(message='Hours and Minutes must be standardized! Read the "Data" at the official '
                                  'documentation.', code=2)

    if (int(hours) < 7 or int(hours) > 19) or (int(minutes) != 30 and int(minutes) != 0):
        raise InvalidPost(message='Hours and Minutes must be standardized! Read the "Data" at the official '
                                  'documentation.', code=2)


def handle_request_post_data_to_api_schedule(request):
    # Standard checks
    keys = ['day', 'month', 'year', 'hours', 'minutes', 'company-name', 'token-id']
    for key in keys:
        if not request.POST.get(key):
            raise InvalidPost(message='Invalid or Missing Post Data.', code=1)

    """ How the following data should looks like:
    Day: 25
    Month: 10
    Year: 2020
    Hours: 18
    Minutes: 59
    Company Name: Dr4kk0nnys Inc.
    Token Id: iu32rh2irh3uh3asd1h8478yq7ya1sd1h3j9ha0sa2sd8uh6if00jd7uh123uh12h312jh
    """  # Stupid time-variables ...
    day = request.POST['day']
    month = request.POST['month']
    year = request.POST['year']

    is_date_valid(day, month, year)

    hours = request.POST['hours']
    minutes = request.POST['minutes']

    is_time_valid(hours, minutes)

    # name of the company for organization's sake
    company_name = request.POST['company-name']

    token_id = request.POST['token-id']

    if not User.objects.filter(token_id=token_id):
        raise InvalidTokenId()

    return {
        'day': day,
        'month': month,
        'year': year,
        'hours': hours,
        'minutes': minutes,
        'company-name': company_name,
        'token-id': token_id
    }


def convert_datetime_string_to_datetime_object(post_request, months):
    datetime_string = f'{months[int(post_request["month"]) - 1]} {post_request["day"]} {post_request["year"]} ' \
                      f'{post_request["hours"]}:{post_request["minutes"]}'

    # passing all the variables to a datetime object
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    return datetime_object


def was_meeting_scheduled_to_a_saturday_or_sunday(datetime_object):
    # get the week day of the datetime_object date
    # monday = 0, tuesday = 1, ..., saturday = 5, sunday = 6
    datetime_weekday = datetime.weekday(datetime_object)

    if datetime_weekday >= 5:
        return True
    return False


def was_meeting_scheduled_to_the_past(datetime_object):
    current_date = datetime.now()

    if current_date > datetime_object:  # AKA, if it's in the past
        return True

    return False


def is_meeting_scheduled_time_available(datetime_object):
    """
    Date objects from database should look like this:
    < QuerySet[] >:
        [0]: { Date, Count }
        Date should look like:
            year-month-day: 2020-10-30
        Count should look like:
            int: 1

    Date datetime should look like this:
        year-month-day: 2020-10-30
    Time datetime should look like this:
        hours:minutes:seconds: 04:20:00

    Datetime object:
        '2020-10-30 04:20:00'
    """
    date_objects_from_database = ScheduledDate.objects.all()

    date_datetime = str(datetime_object).split(' ')[0]
    time_datetime = str(datetime_object).split(' ')[1]

    for scheduled_date in date_objects_from_database:
        date = str(scheduled_date).split(' ')[0]
        time = str(scheduled_date).split(' ')[1]

        # if they're on the same day
        if date == date_datetime:

            # if they're on the same time ( both hours and minutes )
            if time == time_datetime:

                count = 3
                if time_datetime <= '11:30:00':
                    count = 5

                # if less than {count} people already scheduled to this time, schedule it normally
                if ScheduledDate.objects.select_for_update().get(date=datetime_object).count < count:
                    return True
                return False

    return True


def is_datetime_already_on_the_database(datetime_object):
    try:
        ScheduledDate.objects.get(date=datetime_object)
    except ObjectDoesNotExist:
        return False
    return True


def get_json_response(success, data, error):
    return {
        "success": success,
        "data": data,
        "error": error
    }


def handle_post_request_to_api_time(request):
    keys = ['day', 'month', 'year', 'token-id']
    for key in keys:
        if not request.POST[key]:
            raise InvalidPost(message="Invalid or Missing Post Data", code=1)

    day = request.POST['day']
    month = request.POST['month']
    year = request.POST['year']

    is_date_valid(day, month, year)

    token_id = request.POST['token-id']

    if not User.objects.filter(token_id=token_id):
        raise InvalidTokenId()

    return {
        'day': day,
        'month': month,
        'year': year,
        'token-id': token_id
    }


def increase_user_api_calls_if_is_smaller_than_15(token_id):
    # Checking user api calls first, so no ddos attack can be done
    user = User.objects.select_for_update().get(token_id=token_id)
    if user.api_calls >= 15:
        raise InvalidApiCall()

    user.api_calls = F('api_calls') + 1
    user.save()
