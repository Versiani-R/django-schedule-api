from django.shortcuts import render, redirect
from django.db.models import F
from django.http import JsonResponse, HttpResponse

from .utils import *
from .authentication import generate_hash, generate_token
from .exceptions import InvalidPost, InvalidTokenId
from .models import ScheduledDate, User


# TODO: Do the documentation

# TODO: Implement the new api logic:
# TODO: All functions must return a json
# TODO: Work on the authentication of requests

# TODO: Standardize the JSON Response

# TODO: Delete junk files

# TODO: Create pyautogui test for the multiple request at the same time


def index(request):
    return render(request, 'api/index.html')


def register(request):
    return render(request, 'api/register.html')


# TODO: Do a few more checks to the email and password
def handle_register(request):

    if ('email' and 'password') not in request.POST:
        return HttpResponse('Invalid post data.')

    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(email=email):
        return HttpResponse('Email already registered.')

    if len(password) < 6:
        return HttpResponse('Password too short. It must be at least 6 characters long.')

    hashed_password = generate_hash(password)
    token_id = generate_token(email, password)

    User.objects.get_or_create(email=email, password=hashed_password, token_id=token_id)

    return render(request, 'api/register_success.html', {"token_id": token_id})


def api_schedule(request):

    try:
        post_request = handle_request_post_data_to_api_schedule(request)
    except InvalidPost:
        return JsonResponse({"invalid": "true"})
    except InvalidTokenId:
        return JsonResponse({"invalidTokenId": "true"})

    datetime_object = convert_datetime_string_to_datetime_object(post_request, months=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
    )

    """
    For documentation of the following checks, please refer to the comments on the functions:
    **Note**: They were moved to the utils.py file!
        * was_meeting_scheduled_to_a_saturday_or_sunday
        * was_meeting_scheduled_to_the_past
        * is_meeting_scheduled_time_available
    """
    if was_meeting_scheduled_to_a_saturday_or_sunday(datetime_object):
        return redirect('schedule_error', error_code=2)
    if was_meeting_scheduled_to_the_past(datetime_object):
        return redirect('schedule_error', error_code=3)

    try:
        (is_available, database_object) = is_meeting_scheduled_time_available(datetime_object)

        # TODO: Increment the value of api_calls of the user
        if is_available:
            database_object.count = F('count') + 1
            database_object.name_set.create(name=post_request['company_name'])
            database_object.save()
        else:
            return redirect('schedule_error', error_code=4)
    except TypeError:
        """
        TypeError occurs when the database_object is empty ( nothing on the database )
        If that's the case, we need to create a brand new object to an empty database.
        """
        ScheduledDate.objects.get_or_create(date=datetime_object)
        database_object = ScheduledDate.objects.select_for_update().get(date=datetime_object)
        database_object.name_set.create(name=post_request['company_name'])
        database_object.save()

    """
    No more need to keep track of current time zone.
    Since USE_TZ is now set to False, and the timezone code
    is correct ('America/Sao_Paulo'), there isn't need to
    make the datetime object aware.
    
    The code will remain commented for knowledge sake. 
    """
    # current_timezone = timezone.get_current_timezone()
    # print(f'Current timezone: {current_timezone}')
    # timezone_aware_date = current_timezone.localize(datetime_object)
    # print(f'Timezone aware date: {timezone_aware_date}')

    return JsonResponse({"success": "true"})

    # return redirect(
    #     'schedule_success',
    #     post_request['day'],
    #     post_request['month'],
    #     post_request['year'],
    #     post_request['hours'],
    #     post_request['minutes'],
    #     post_request['company_name'],
    # )

#
# def api_error(request, error_code):
#     return render(request, 'api/schedule_error.html', {'error_code': error_code})
#
#
# def api_success(request, day, month, year, hours, minutes, company_name):
#     return render(request, 'api/schedule_success.html', {
#         'day': day,
#         'month': month,
#         'year': year,
#         'hours': hours,
#         'minutes': minutes,
#         'company_name': company_name
#     })
