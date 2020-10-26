from django.test import TestCase
from django.test.client import Client

from django.utils import timezone

from django.contrib.auth.models import User

from datetime import datetime

from .models import ScheduledDate


class CheckAdminUserTests(TestCase):
    def test_check_admin_user_as_default_user(self):
        """
        If a default user tries to access the api/detail,
        The user must be redirected.
        """
        client = Client()
        response = client.get('/api/detail/')
        self.assertEqual(response.status_code, 302)

    def test_check_admin_user_as_admin_user(self):
        """
        If a super user ( admin ) tries to access the api/detail,
        It should load normally.
        """
        my_admin_password = '1-2-3-4-5'
        my_admin = User.objects.create_superuser('dr4kk0nnys', 'renatoversianidrakk@gmail.com', my_admin_password)
        client = Client()
        client.login(username=my_admin.username, password=my_admin_password)
        response = client.get('/api/detail/')
        self.assertEqual(response.status_code, 200)


def create_scheduled_date():
    datetime_string = 'Oct 25 2066 16:20'
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    current_timezone = timezone.get_current_timezone()
    timezone_aware_date = current_timezone.localize(datetime_object)

    company_name = 'Dr4kk0 Inc.'

    # making sure it was created, if it wasn't on the database already
    ScheduledDate.objects.get_or_create(date=timezone_aware_date, name=company_name)

    new_scheduled_date = ScheduledDate.objects.get_or_create(date=timezone_aware_date, name=company_name)

    return new_scheduled_date


class CheckRequestHandleTests(TestCase):
    def test_handle_request_data_with_saturday_date_value(self):
        """
        A post request with a date to a saturday or sunday
        should redirect the client to /api/error/2 ( Error code 2: Schedule to a saturday or a sunday ).

        Read more on the api/templates/api/schedule_error.html
        """
        response = self.client.post('/api/schedule/', {
            'date': '2006-10-28',
            'hours': 16,
            'minutes': 20,
            'name': 'Dr4kk0 Inc.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/error/2/')

    def test_handle_request_data_with_past_date_value(self):
        """
        A post request with a past date should redirect
        the user to /api/error/3 ( Error code 3: Schedule to the past ).

        Read more on the api/templates/api/schedule_error.html
        """
        response = self.client.post('/api/schedule/', {
            'date': '2006-10-25',
            'hours': 16,
            'minutes': 20,
            'name': 'Dr4kk0 Inc.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/error/3/')

    def test_handle_post_request_data_with_already_scheduled_value(self):
        """
        A post request with a date that is already scheduled
        should redirect the user to /api/error/4

        Read more on the api/templates/api/schedule_error.html
        """
        create_scheduled_date()

        response = self.client.post('/api/schedule/', {
            'date': '2066-10-25',
            'hours': 16,
            'minutes': 20,
            'name': 'Dr4kk0 Inc.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/error/4/')


class CheckDatabaseHandleTests(TestCase):
    def test_handle_database_creation_with_already_existing_value(self):
        """
        Creating a new scheduled meeting in the database
        when there is a meeting already booked should not
        work, and the meeting shall not be created.
        """
        create_scheduled_date()
        new_scheduled_date = create_scheduled_date()
        self.assertEqual(new_scheduled_date[1], False)
