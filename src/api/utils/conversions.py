from datetime import datetime


def convert_datetime_string_to_datetime_object(post_request, months):
    datetime_string = f'{months[int(post_request["month"]) - 1]} {post_request["day"]} {post_request["year"]} ' \
                      f'{post_request["hours"]}:{post_request["minutes"]}'

    # passing all the variables to a datetime object
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    return datetime_object
