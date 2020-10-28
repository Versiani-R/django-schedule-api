from datetime import datetime

from .models import User, ScheduledDate
from .exceptions import InvalidPost, InvalidTokenId


def is_token_id_valid(token_id):
    if User.objects.filter(token_id=token_id):
        return True
    return False


def handle_request_post_data_to_api_schedule(request):
    # Standard checks
    keys = ['day', 'month', 'year', 'hours', 'minutes', 'name', 'token-id']
    for key in keys:
        if not request.POST.get(key):
            raise InvalidPost(message='Invalid or Missing Post Data.', code=1)

    """
    Date is a html input, whose type is 'date'
    It looks like this: 10-25-2020 (mm-dd-yyyy)

    Day: 25
    Month: 10
    Year: 2020


    Hours: 18
    Minutes: 59
    """  # Stupid time-variables ...
    day = request.POST['day']
    month = request.POST['month']
    year = request.POST['year']

    if len(day) != 2 or len(month) != 2:
        raise InvalidPost(message='Day and Month must be standardized! Read the "Data" at the official documentation.',
                          code=2)
    if len(year) != 4:
        raise InvalidPost(message='Year must be standardized! Read the "Data" at the official documentation.', code=2)

    if 1 > int(day) > 31 or 1 > int(month) > 12:
        raise InvalidPost(message='Day or Month value is incorrect! Read the "Data" at the official documentation.',
                          code=2)

    hours = request.POST['hours']
    minutes = request.POST['minutes']

    if len(hours) != 2 or len(minutes) != 2:
        raise InvalidPost(message='Hours and Minutes must be standardized! Read the "Data" at the official '
                                  'documentation.', code=2)
    if 1 > int(hours) > 23 or 1 > int(minutes) > 59:
        raise InvalidPost(message='Hours and Minutes must be standardized! Read the "Data" at the official '
                                  'documentation.', code=2)

    # name of the company for organization's sake
    company_name = request.POST['name']

    token_id = request.POST['token-id']

    if not is_token_id_valid(token_id):
        raise InvalidTokenId()

    return {
        'day': day,
        'month': month,
        'year': year,
        'hours': hours,
        'minutes': minutes,
        'company_name': company_name,
    }


def convert_datetime_string_to_datetime_object(post_request, months):
    print(f'Testing: {post_request["month"]}')
    datetime_string = f'{months[int(post_request["month"]) - 1]} {post_request["day"]} {post_request["year"]} ' \
                      f'{post_request["hours"]}:{post_request["minutes"]}'

    # passing all the variables to a datetime object
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    return datetime_object


def was_meeting_scheduled_to_a_saturday_or_sunday(datetime_object):
    """ Check 1: Checking if the meeting was scheduled to a saturday or to a sunday.
    The month variable is not 0 index ( html values ... ).
    Because of that, datetime_string has to consider the month value, and subtract 1.
    ( months[int(post_request["month"]) - 1] ).
    All those datetime variables were created in order to check the day of the date object passed through the html.
    datetime.weekday requires a datetime object and returns an integer.
    This integer is the 0-index-based value of the days of the week.
    So, monday = 0, tuesday = 1, ... saturday = 5, sunday = 6.
    Then, it simply checks if the datetime_weekday variable is greater than 5, if so, it's either a saturday or sunday.
    """

    # get the week day of the datetime_object date
    # monday = 0, tuesday = 1, ..., saturday = 5, sunday = 6
    datetime_weekday = datetime.weekday(datetime_object)

    if datetime_weekday >= 5:
        return True

    return False


def was_meeting_scheduled_to_the_past(datetime_object):
    """ Check 2: Check if the meeting was scheduled to the past

        It takes usage of the datetime_object previously created to check 1.

        Datetime objects in general are 'weird'. The newer it is, the greater it is.
        So, a datetime object for like '2006 Jun 12 13:30PM' is smaller than '2012 Jun 12 13:30PM'.
        With that in mind, we check for the current date (datetime.now()) and compare with the datetime object.
        If the current date is greater than the datetime_object, the datetime_object is in the past.
        """
    current_date = datetime.now()

    if current_date > datetime_object:  # AKA, if it's in the past
        return True

    return False


def is_meeting_scheduled_time_available(datetime_object):
    """ Check 3: Check if day and hour is available, and then check if there's no over than 5 meetings scheduled.

        Retrieve all the scheduled_dates from the database and compare with the datetime_object.
        If a match on the day is found, it checks for the time, if a match occurs, then they're scheduled for the same
        time.

        sanitized_scheduled_date[0] is the same as the date, it looks like this:
            * sanitized_scheduled_date[0]:  '2020-10-29'
            * sanitized_datetime_object[0]: '2020-10-29'

        sanitized_scheduled_date[1] is the same as the time, it looks like this:
            * sanitized_scheduled_time:  '12:00:00'
            * sanitized_datetime_object[1]: '12:00:00'

        **Note**: Since the user can only schedule a meeting on either 0 or 30 minutes, it's really not necessary to
        check  for hours and only after that, minutes. That's why the time itself is compared, and not hours,
        and only then, minutes.
        """
    scheduled_dates = ScheduledDate.objects.all()

    sanitized_datetime_object = str(datetime_object).split(' ')

    for scheduled_date in scheduled_dates:
        sanitized_scheduled_date = str(scheduled_date).split(' ')

        """
        * Check if the 5 doctors logic is correct

        Both sanitized dates have the same format: year-month-day.
        Check for the day, if they're on the same day, check for the time.
        If they're on the same time, check for the database_object.count value.

        The business rule here is:
            * This 'count' value cannot be greater than 5.

        If the value is smaller than or equals 4, we can add one more schedule.

        **Note**: The whole code should be race-condition-issue free.
        **Note**: The database_object is the value retrieved from the database itself. 
            What does that mean ?
            It means that the select_for_update() freezes the database for the transaction.
                * Again, it should be race-condition-issue free. 
            We then increase the count value ( number of meetings scheduled )
            Push the name of the business name ( Company Name ) to the array of names in the database.
            We then save it, closing the 'freeze' time.
        """
        # if they're on the same day
        if sanitized_scheduled_date[0] == sanitized_datetime_object[0]:
            sanitized_scheduled_time = str(scheduled_date).split(' ')[1].split('+')[0]

            # if they're on the same time ( both hours, and minutes )
            if sanitized_scheduled_time == sanitized_datetime_object[1]:

                # database_object is the object value retrieved through the database itself
                database_object = ScheduledDate.objects.select_for_update().get(date=datetime_object)

                count = 3
                if sanitized_datetime_object[1] <= '11:30:00':
                    count = 5

                # if less than {count} people already scheduled to this time, schedule it normally
                if database_object.count < count:
                    print(f'Count value is: {count}')
                    print(f'Sanitized datetime object is: {sanitized_datetime_object[1]}')
                    return True, database_object

                else:
                    return False, database_object


def get_json_response(success, data, error):
    return {
        "success": success,
        "data": data,
        "error": error
    }
