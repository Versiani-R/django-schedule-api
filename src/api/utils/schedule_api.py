from django.db.models import F

from ..models import User
from .exceptions import InvalidApiCall


def increase_api_calls(token_id):
    user = User.objects.select_for_update().get(token_id=token_id)
    if user.api_calls >= 15:
        raise InvalidApiCall()

    user.api_calls = F('api_calls') + 1
    user.save()
