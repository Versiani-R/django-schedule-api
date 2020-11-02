from django.db.models import F

from ..models import User

from .exceptions import InvalidPost, InvalidTokenId, InvalidApiCall
from .validations import is_date_valid, is_time_valid


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


def increase_user_api_calls_if_is_smaller_than_15(token_id):
    # Checking user api calls first, so no ddos attack can be done
    user = User.objects.select_for_update().get(token_id=token_id)
    if user.api_calls >= 15:
        raise InvalidApiCall()

    user.api_calls = F('api_calls') + 1
    user.save()
