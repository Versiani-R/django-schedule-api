from datetime import datetime


def convert_datetime_string_to_datetime_object(day, month, year, hours, minutes, months):
    datetime_string = f'{months[int(month) - 1]} {day} {year} {hours}:{minutes}'

    # passing all the variables to a datetime object
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    return datetime_object
