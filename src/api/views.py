from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import F

from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response


from api.serializers import RegisterSerializer, ScheduleSerializer

from api.utils.validations import is_date_valid

from .utils.api_schedule import handle_request_post_data_to_api_schedule, increase_user_api_calls_if_is_smaller_than_15
from .utils.api_time import handle_post_request_to_api_time
from .utils.exceptions import InvalidPost, InvalidTokenId, InvalidApiCall
from .utils.json_response import get_json_response
from .utils.conversions import convert_datetime_string_to_datetime_object
from .utils.validations import was_meeting_scheduled_to_a_saturday_or_sunday, \
    was_meeting_scheduled_to_the_past, \
    is_meeting_scheduled_time_available, \
    is_datetime_already_on_the_database

from .authentication import generate_hash, generate_token
from .models import ScheduledDate, User

# from .threading import reset_api_calls_after_15_minutes

# from .spreadsheet import *


def index(request):
    return render(request, 'api/index.html')


class RegisterView(APIView):
    """
    Return the register template if is a GET request.
    Handle the register if is a POST request.
    """
    def get(self, request):
        return render(request, 'api/register.html')
    
    def post(self, request, pk=None, format=None):
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(get_json_response("false", {}, {"code": 1, "message": "Invalid or Incorrect data on the post request."}))

        [email, password] = [item for item in serializer.data.values()]

        # Checking if the email is already registered.
        if User.objects.filter(email=email):
            return Response(get_json_response("false", {}, {"code": 2, "message": "Invalid or Incorrect credentials. Email already registered."}))

        # Checking if the password is strong
        if not len(password) > 5:
            return Response(get_json_response("false", {}, {"code": 3, "message": "Invalid or Incorrect credentials. Weak credentials."}))

        [hashed_password, token_id] = [generate_hash(serializer.data['password']), generate_token(email, password)]

        User.objects.get_or_create(email=email, password=hashed_password, token_id=token_id)

        return Response(get_json_response("true", {"email": email, "token-id": token_id}, {}))


class ScheduleApiView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    Return the scheduled meetings of the day passed. GET request.
    Create a schedule through the POST request.
    """
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        [year, month, day] = [item for item in self.kwargs.values()]

        return ScheduledDate.objects.filter(date__startswith='-'.join([year, month, day]))
    
    def get(self, request, *args, **kwargs):
        [year, month, day] = [item for item in self.kwargs.values()]

        try:
            is_date_valid(day, month, year)
        except InvalidPost as invalid_post:
            return Response(get_json_response("false", {}, {"code": 2, "message": invalid_post.message}))

        return self.list(request, *args, **kwargs)


    # def get(self, request, test, pk=None, format=None):
    #     print(test)
    #     return JsonResponse({"Yeay": "true"})


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

    database_object = ScheduledDate.objects.select_for_update().get(date=datetime_object)

    database_object.count = F('count') + 1
    database_object.save()

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
