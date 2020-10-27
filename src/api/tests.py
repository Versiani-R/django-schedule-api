from django.test import TestCase
from django.test.client import Client
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

    # making sure it was created
    new_scheduled_date_object = ScheduledDate.objects.get_or_create(date=datetime_object)
    scheduled_object = ScheduledDate.objects.get(date=datetime_object)

    return new_scheduled_date_object, scheduled_object


def create_and_update_scheduled_date():
    datetime_string = 'Oct 25 2066 16:20'
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    create_scheduled_date()

    # updating the new one, since it already exists
    new_scheduled_date = ScheduledDate.objects.select_for_update().get(date=datetime_object)
    new_scheduled_date.count += 1
    new_scheduled_date.name_set.create(name='Fake Business for tests only.')
    new_scheduled_date.save()

    scheduled_date_object = ScheduledDate.objects.get(date=datetime_object)

    return scheduled_date_object


# Requires creation
def update_scheduled_date():
    datetime_string = 'Oct 25 2066 16:20'
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    new_scheduled_date = ScheduledDate.objects.select_for_update().get(date=datetime_object)
    new_scheduled_date.count += 1
    new_scheduled_date.name_set.create(name='Fake Business for tests only.')
    new_scheduled_date.save()

    scheduled_date_object = ScheduledDate.objects.get(date=datetime_object)

    return scheduled_date_object


def get_response_object_before_11_30():
    return {
        'date': '2065-10-28',
        'hours': 10,
        'minutes': 20,
        'name': 'Dr4kk0 Inc.'
    }


def get_response_object_at_11_30():
    return {
        'date': '2065-10-28',
        'hours': 11,
        'minutes': 30,
        'name': 'Dr4kk0 Inc.'
    }


def get_response_object_after_11_30():
    return {
        'date': '2065-10-28',
        'hours': 16,
        'minutes': 20,
        'name': 'Dr4kk0 Inc.'
    }


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
        """ Old logic ( following old business rule )
        A post request with a date that is already scheduled
        should redirect the user to /api/error/4

        Read more on the api/templates/api/schedule_error.html
        """

        """ New logic ( following current business rule )
        A post request with a date that is already scheduled
        should redirect the user to /api/success/ if the
        database_object.count value is less than 5
        """
        create_scheduled_date()

        response = self.client.post('/api/schedule/', {
            'date': '2066-10-25',
            'hours': 16,
            'minutes': 20,
            'name': 'Dr4kk0 Inc.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/success/25-10-2066/16-20/Dr4kk0%20Inc./')

    def test_handle_post_request_data_with_five_scheduled_values_before_11_30(self):
        """ Old logic ( following old business rule )
        5 post requests with a date that is already scheduled
        should redirect the user to /api/success/
        """

        """ New logic ( following current business rule )
        5 post requests with a date that is already scheduled
        and the time is less than or equals 11:30 should
        redirect the user to /api/success/
        """

        for i in range(5):
            response = self.client.post('/api/schedule/', get_response_object_before_11_30())

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/api/success/28-10-2065/10-20/Dr4kk0%20Inc./')

    def test_handle_post_request_data_with_five_scheduled_values_at_11_30(self):
        """ Old logic ( following old business rule )
        5 post requests with a date that is already scheduled
        should redirect the user to /api/success/
        """

        """ New logic ( following current business rule )
        5 post requests with a date that is already scheduled
        and the time is less than or equals 11:30 should
        redirect the user to /api/success/
        """

        for i in range(5):
            response = self.client.post('/api/schedule/', get_response_object_at_11_30())

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/api/success/28-10-2065/11-30/Dr4kk0%20Inc./')

    def test_handle_post_request_data_with_three_scheduled_values_after_11_30(self):
        """ Old logic ( following old business rule )
        5 post requests with a date that is already scheduled
        should redirect the user to /api/success/
        """

        """ New logic ( following current business rule )
        3 post requests with a date that is already scheduled
        and the time is greater than 11:30 should
        redirect the user to /api/success/
        """

        for i in range(3):
            response = self.client.post('/api/schedule/', get_response_object_after_11_30())

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/api/success/28-10-2065/16-20/Dr4kk0%20Inc./')

    def test_handle_post_request_data_with_five_scheduled_values_after_11_30(self):
        """ Old logic ( following old business rule )
        5 post requests with a date that is already scheduled
        should redirect the user to /api/success/
        """

        """ New logic ( following current business rule )
        5 post requests with a date that is already scheduled
        and the time is greater than 11:30 should
        redirect the user to /api/error/4/
        """

        for i in range(3):
            response = self.client.post('/api/schedule/', get_response_object_after_11_30())

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/api/success/28-10-2065/16-20/Dr4kk0%20Inc./')

        response = self.client.post('/api/schedule/', get_response_object_after_11_30())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/error/4/')

    def test_handle_post_request_data_with_six_scheduled_values(self):
        """
        6 post requests with a date that is already scheduled
        should redirect the user to /api/error/4
        """

        for i in range(5):
            response = self.client.post('/api/schedule/', {
                'date': '2066-10-25',
                'hours': 11,
                'minutes': 20,
                'name': 'Dr4kk0 Inc.'
            })

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/api/success/25-10-2066/11-20/Dr4kk0%20Inc./')

        response = self.client.post('/api/schedule/', {
            'date': '2066-10-25',
            'hours': 11,
            'minutes': 20,
            'name': 'Dr4kk0 Inc.'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/api/error/4/')


class CheckDatabaseHandleTests(TestCase):
    """ Old logic ( following old business rule )
    Creating a new scheduled meeting in the database
    when there is a meeting already booked should not
    work, and the meeting shall not be created.
    """

    """ New logic ( following current business rule )
    Creating a new scheduled meeting in the database
    when there is a meeting already booked should work
    if the count value is smaller than 5.
    """

    def test_handle_database_creation_with_no_existing_value(self):
        """
        Creating a new schedule when there is no existing
        object in the database should return true. Since
        the object was in fact created.
        """
        (scheduled_date_object, _) = create_scheduled_date()
        self.assertEqual(scheduled_date_object[1], True)

    def test_handle_database_creation_with_already_existing_value(self):
        """
        Creating a new schedule when there is already a existing
        schedule object in the database should return False, since
        the object is not brand new.
        """
        (first_object, _) = create_scheduled_date()
        (second_object, _) = create_scheduled_date()

        self.assertEqual(first_object[1], True)
        self.assertEqual(second_object[1], False)

    def test_handle_database_create_count_value(self):
        """
        Creating an object in the database with empty
        name and count, should create an object with
        default values:

        Name: 'Fake Business for tests only.'
        Count: 1
        """
        (_, scheduled_object) = create_scheduled_date()

        self.assertEqual(scheduled_object.count, 1)

    def test_handle_database_create_and_update_name_and_value(self):
        """
        Creating a new object in the database should set the
        count to 1. Adding a new object should increase the value to
        2. And updating the name on the database should set the
        name to the updated name.
        """

        scheduled_date_object = create_and_update_scheduled_date()

        self.assertEqual(scheduled_date_object.count, 2)
        self.assertEqual(scheduled_date_object.name_set.all()[0].name, 'Fake Business for tests only.')

    def test_handle_database_creating_5_schedules(self):
        """
        The database should be able to create 5 schedules
        to a same time.
        """
        (first_object, scheduled_date) = create_scheduled_date()

        self.assertEqual(first_object[1], True)
        self.assertEqual(scheduled_date.count, 1)

        for i in range(2, 6):
            scheduled_date = update_scheduled_date()
            self.assertEqual(scheduled_date.count, i)
        #
        # scheduled_date = update_scheduled_date()
        # self.assertEqual(scheduled_date.count, 3)
        #
        # scheduled_date = update_scheduled_date()
        # self.assertEqual(scheduled_date.count, 4)
        #
        # scheduled_date = update_scheduled_date()
        # self.assertEqual(scheduled_date.count, 5)
