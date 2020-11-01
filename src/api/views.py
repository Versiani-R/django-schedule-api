from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .utils import *
from .authentication import generate_hash, generate_token
from .exceptions import InvalidPost, InvalidTokenId
from .models import ScheduledDate
# from .threading import reset_api_calls_after_15_minutes

from .spreadsheet import *
# get_user_weekly_metrics('32216007444142488f967168546c00455cbf1164196c4087b9af9cde44b2fde4', 5, 11, 2020)
# get_total_schedules_from_two_accounts(
#   '32216007444142488f967168546c00455cbf1164196c4087b9af9cde44b2fde4',
#   'a808b45dc0e0b589a90766973be95de52b83a92e14aaa4ff19ca7f4b38064729'
# )
# get_user_entire_average_schedule_by_day('32216007444142488f967168546c00455cbf1164196c4087b9af9cde44b2fde4')
# get_user_monthly_average_schedule_by_day(
#     '32216007444142488f967168546c00455cbf1164196c4087b9af9cde44b2fde4',
#     2020,
#     11
# )
call_three_users_at_the_same_time(
    '2020-11-05 11:30:00',
    '2020-11-05 14:30:00',
    '32216007444142488f967168546c00455cbf1164196c4087b9af9cde44b2fde4',
    'a808b45dc0e0b589a90766973be95de52b83a92e14aaa4ff19ca7f4b38064729',
    '4ef38a7062482d6f782f1db5ac729bf5d3ef97b626b3df45135f3756ce85d3b4'
)


def index(request):
    return render(request, 'api/index.html')


def register(request):
    return render(request, 'api/register.html')


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

    except InvalidPost as invalid_post:
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": invalid_post.code,
                "message": invalid_post.message
            }
        )
        return JsonResponse(json_response)

    except InvalidTokenId:
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 3,
                "message": "Invalid Token Id."
            }
        )
        return JsonResponse(json_response)

    datetime_object = convert_datetime_string_to_datetime_object(post_request, months=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
    )

    try:
        increase_user_api_calls_if_is_smaller_than_15(post_request['token-id'])
    except InvalidApiCall:
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 7,
                "message": "Number of api calls made in 15 minutes is over the allowed quantity."
            }
        )
        return JsonResponse(json_response)

    """
    For documentation of the following checks, please refer to the comments on the functions:
    **Note**: They were moved to the utils.py file!
        * was_meeting_scheduled_to_a_saturday_or_sunday
        * was_meeting_scheduled_to_the_past
        * is_meeting_scheduled_time_available
    """
    if was_meeting_scheduled_to_a_saturday_or_sunday(datetime_object):
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 4,
                "message": "Cannot Schedule a meeting to a saturday or sunday."
            }
        )
        return JsonResponse(json_response)

    if was_meeting_scheduled_to_the_past(datetime_object):
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 5,
                "message": "Cannot Schedule a meeting to the past."
            }
        )
        return JsonResponse(json_response)

    if not is_meeting_scheduled_time_available(datetime_object):
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 6,
                "message": "Number of meetings scheduled to the date and hour is over the allowed number."
            }
        )
        return JsonResponse(json_response)

    if not is_datetime_already_on_the_database(datetime_object):
        ScheduledDate.objects.get_or_create(date=datetime_object)

    user = User.objects.select_for_update().get(token_id=post_request['token-id'])
    database_object = ScheduledDate.objects.select_for_update().get(date=datetime_object)

    database_object.count = F('count') + 1
    database_object.information_set.create(
        name=post_request['company-name'],
        token_id=post_request['token-id'],
        email=user.email
    )
    database_object.save()

    user.schedules_set.create(date_and_time=datetime_object)

    json_response = get_json_response(
        success="true",
        data={
            "date": f"{post_request['day']}-{post_request['month']}-{post_request['year']}",
            "time": f"{post_request['hours']}:{post_request['minutes']}",
            "company-name": post_request['company-name']
        },
        error={}
    )
    return JsonResponse(json_response)


def api_time(request):
    try:
        post_request = handle_post_request_to_api_time(request)
    except InvalidPost as invalid_post:
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": invalid_post.code,
                "message": invalid_post.message
            }
        )
        return JsonResponse(json_response)

    except InvalidTokenId:
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 3,
                "message": "Invalid Token Id."
            }
        )
        return JsonResponse(json_response)

    try:
        increase_user_api_calls_if_is_smaller_than_15(post_request['token-id'])
    except InvalidApiCall:
        json_response = get_json_response(
            success="false",
            data={},
            error={
                "code": 7,
                "message": "Number of api calls made in 15 minutes is over the allowed quantity."
            }
        )
        return JsonResponse(json_response)

    day = post_request['day']
    month = post_request['month']
    year = post_request['year']

    query = ScheduledDate.objects.filter(date__startswith='-'.join([year, month, day]))
    database_objects = []

    for entrance in query:
        database_objects.append(f'{entrance}: {entrance.count}')

    json_response = get_json_response(
        success="true",
        data=database_objects,
        error={}
    )
    return JsonResponse(json_response)
