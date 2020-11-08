from django.db.models import F

from api.models import User
from api.utils.exceptions import InvalidApiCall


def decrease_api_calls(token_id):
    user = User.objects.select_for_update().get(token_id=token_id)
    if user.api_calls <= 0:
        raise InvalidApiCall()

    user.api_calls = F('api_calls') - 1
    user.save()
