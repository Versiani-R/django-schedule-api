from ..models import User

from .exceptions import InvalidPost, InvalidTokenId
from .validations import is_date_valid


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
