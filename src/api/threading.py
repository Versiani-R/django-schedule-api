from threading import Timer

from .models import User

from django.db.models import F


# Reset all api calls after 15 minutes
def reset_api_calls_after_15_minutes():
    users_with_api_calls_greater_than_1 = User.objects.filter(api_calls__gte=1)

    print('Yolooooooooooooooooooooooooooooooooooooooo')

    for user in users_with_api_calls_greater_than_1:
        user.api_calls = F('api_calls') * 0
        user.save()

    # Timer(60.0 * 15, reset_api_calls_after_15_minutes).start()


# reset_api_calls_after_15_minutes()
