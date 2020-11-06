from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import F
from django.forms.models import model_to_dict

from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response


from api.serializers import RegisterSerializer, TimeListSerializer, ScheduleApiSerializer

from api.utils.validations import *

from .utils.api_schedule import handle_request_post_data_to_api_schedule, increase_api_calls
from .utils.api_time import handle_post_request_to_api_time
from .utils.exceptions import InvalidPost, InvalidTokenId, InvalidApiCall
from .utils.json_response import get_json_response
from .utils.conversions import convert_datetime_string_to_datetime_object
from .utils.validations import is_meeting_scheduled_time_available, is_datetime_already_on_the_database

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


class TimeListView(APIView):
    def post(self, request, pk=None, format=None):
        serializer = TimeListSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(get_json_response("false", {}, {"code": 1, "message": "Invalid or Incorrect data on the post request."}))
        
        [day, month, year, token_id] = serializer.data.values()

        try:
            is_date_valid(day, month, year)
            is_token_id_valid(token_id)
            increase_api_calls(token_id)
        except InvalidPost as e:
            return Response(e.format_invalid_post())

        except InvalidTokenId as e:
            return Response(e.format_invalid_token_id())

        except InvalidApiCall as e:
            return Response(e.format_invalid_api_call())

        return Response(get_json_response("true", ScheduledDate.objects.filter(date__startswith='-'.join([year, month, day])).values(), {}))


class ScheduleApi(APIView):
    def post(self, request, pk=None, format=None):
        serializer = ScheduleApiSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(get_json_response("false", {}, {"code": 1, "message": "Invalid or Incorrect data on the post request."}))
        
        [day, month, year, hours, minutes, company_name, token_id] = serializer.data.values()

        # TODO: The code bellow repeats, make a function on the utils folder for it.
        try:
            is_date_valid(day, month, year)
            is_token_id_valid(token_id)
            increase_api_calls(token_id)
        except InvalidPost as e:
            return Response(e.format_invalid_post())

        except InvalidTokenId as e:
            return Response(e.format_invalid_token_id())

        except InvalidApiCall as e:
            return Response(e.format_invalid_api_call())

        try:
            datetime_object = convert_datetime_string_to_datetime_object(day, month, year, hours, minutes, months=[
                'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
            ])

            is_meeting_date_available(datetime_object)
            is_meeting_scheduled_time_available(datetime_object)
            is_datetime_already_on_the_database(datetime_object)
        
        except ValueError:
            return Response(InvalidPost("Invalid or Incorrect data on the post request.", 1).format_invalid_post())

        except InvalidDay as e:
            return Response(e.format_invalid_day())

        except InvalidDate as e:
            return Response(e.format_invalid_date())

        except InvalidTime as e:
            return Response(e.format_invalid_time())

        except InvalidObject:
            ScheduledDate.objects.get_or_create(date=datetime_object)

        database_object = ScheduledDate.objects.select_for_update().get(date=datetime_object)
        database_object.count = F('count') + 1
        database_object.information_set.create(user=User.objects.get(token_id=token_id))
        database_object.save()

        return Response({"Yeay": "success"})
