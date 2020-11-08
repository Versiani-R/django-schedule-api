from django.shortcuts import render
from django.db.models import F

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from api.serializers import RegisterSerializer, TimeListSerializer, ScheduleApiSerializer, ApiCallsSerializer

from api.utils.validations import is_date_and_time_valid, is_datetime_already_on_the_database, is_meeting_date_available
from api.utils.validations import is_meeting_scheduled_time_available, is_token_id_valid

from api.utils.exceptions import *

from api.utils.api_calls import decrease_api_calls
from api.utils.json_response import get_json_response
from api.utils.conversions import convert_datetime_string_to_datetime_object

from api.authentication import generate_hash, generate_token
from api.models import ScheduledDate, User

# from api.spreadsheet import *


# TODO: Make a 'buy' to reset function ( the user must buy the credits to reset it's api calls number )
# TODO: Create a 'logistic way' to convert credits to api calls ( $10 = 10 api calls ? )

def index(request):
    return render(request, 'api/index.html')


class RegisterViewSet(ViewSet):
    """
    Return the register template.
    Handle the register.
    """
    def list(self, request, format=None):
        return render(request, 'api/register.html')
    
    def create(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(InvalidPost("Invalid or Incorrect data on the post request.", 1).display_invalid_exception())

        [email, password] = [item for item in serializer.data.values()]

        # Checking if the email is already registered.
        if User.objects.filter(email=email):
            return Response(get_json_response("false", {}, {"code": 2, "message": "Invalid or Incorrect credentials. Email already registered."}))

        # Checking if the password is strong
        if not len(password) > 5:
            return Response(get_json_response("false", {}, {"code": 3, "message": "Invalid or Incorrect credentials. Weak credentials."}))

        [hashed_password, token_id] = [generate_hash(password), generate_token(email, password)]
        User.objects.get_or_create(email=email, password=hashed_password, token_id=token_id)
        return Response(get_json_response("true", {"email": email, "token_id": token_id}, {}))


class ScheduleApiViewSet(ViewSet):
    """
    List all the schedule meetings to the day.
    Create a new schedule meeting  to the day.
    """
    def validate_basic_information(self, day, month, year, hours, minutes, token_id):
        try:
            is_date_and_time_valid(day, month, year, hours, minutes)
            is_token_id_valid(token_id)
            decrease_api_calls(token_id)
        except InvalidPost as e:
            return Response(e.display_invalid_exception())

        except InvalidTokenId as e:
            return Response(e.display_invalid_exception())

        except InvalidApiCall as e:
            return Response(e.display_invalid_exception())
        
        except:
            return Response(InvalidError().display_invalid_exception())
        
        return None

    def list(self, request, pk=None, format=None):
        serializer = TimeListSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(InvalidPost("Invalid or Incorrect data on the get request.", 1).display_invalid_exception())

        [day, month, year, token_id] = serializer.data.values()
        
        validation = self.validate_basic_information(day, month, year, '08', '00', token_id)
        if validation:
            return validation

        return Response(get_json_response("true", ScheduledDate.objects.filter(date__startswith='-'.join([year, month, day])).values(), {}))

    def create(self, request, pk=None, format=None):
        serializer = ScheduleApiSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(InvalidPost("Invalid or Incorrect data on the post request.", 1).display_invalid_exception())
        
        [day, month, year, hours, minutes, company_name, token_id] = serializer.data.values()

        validation = self.validate_basic_information(day, month, year, hours, minutes, token_id)
        if validation:
            return validation

        try:
            datetime_object = convert_datetime_string_to_datetime_object(day, month, year, hours, minutes, months=[
                'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
            ])

            is_meeting_date_available(datetime_object)
            is_meeting_scheduled_time_available(datetime_object)
            is_datetime_already_on_the_database(datetime_object)
        
        except ValueError:
            return Response(InvalidPost("Invalid or Incorrect data on the post request.", 1).display_invalid_exception())

        except InvalidDay as e:
            return Response(e.display_invalid_exception())

        except InvalidDate as e:
            return Response(e.display_invalid_exception())

        except InvalidTime as e:
            return Response(e.display_invalid_exception())

        except InvalidObject:
            ScheduledDate.objects.get_or_create(date=datetime_object)

        database_object = ScheduledDate.objects.select_for_update().get(date=datetime_object)
        database_object.count = F('count') + 1
        database_object.information_set.create(user=User.objects.get(token_id=token_id))
        database_object.save()

        return Response(get_json_response("true", {
            "date": '-'.join([day, month, year]),
            "time": f"{hours}:{minutes}",
            "company_name": company_name
        }, {}))


class ApiCallsViewSet(ViewSet):
    """
    List  the number of api calls of a certain account
    Reset the number of api calls of a certain account
    """
    def list(self, request, pk=None, format=None):
        serializer = ApiCallsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(InvalidPost("Invalid or Incorrect data on the post request.", 1).display_invalid_exception())

        user = User.objects.filter(token_id=serializer.data['token_id'])

        # Checking if the token id is valid
        if not user:
            return Response(InvalidTokenId().display_invalid_exception())

        return Response(get_json_response("true", {
            "api_calls": user.first().api_calls
        }, {}))

    def create(self, request, pk=None, format=None):
        serializer = ApiCallsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(InvalidPost("Invalid or Incorrect data on the post request.", 1).display_invalid_exception())
        
        try:
            api_credits = serializer.data['api_credits']
        except KeyError:
            return Response(InvalidPost("Invalid or Incorrect data on the post request. Missing or Incorrect api credits value.", 1).display_invalid_exception())

        """
        Api credits will be the value in dollars to be increased in the api calls.
        Ideally, this part would require some authentication and payment methods. I have neither of those.
        Keep in mind that in the real world, in a real api, this part would've been crazy complex.
        Since I'm skipping the authentication and payment parts, it only comes down to actually increase the
        api credits to the api_calls.

        1  api_credits = $1   = api_calls + 1
        50 api_credits = $50  = api_calls + 50
        """
        user = User.objects.filter(token_id=serializer.data['token_id']).first()

        # This variable is for information purpouses, it's being saved here and not bellow the rest of the code
        # to only use one call on the database. Same reason why I'm not calling the decrease_api_credits function.
        api_calls = user.api_calls + int(api_credits)

        user.api_calls = F('api_calls') + int(api_credits)
        user.save()

        return Response(get_json_response("true", {
            "api_credits": api_credits,
            "remaining_api_calls": api_calls
        }, {}))
