from django.test import TestCase

from datetime import datetime

from api.models import ScheduledDate, User


def register_user():
    User.objects.get_or_create(email='blank@gmail.com', password='12345', token_id='token')


def get_json_object(year, hours, minutes="30"):
    return {
        "day": "16",
        "month": "10",
        "year": year,
        "hours": hours,
        "minutes": minutes,
        "company_name": "Dr4kk0 Inc.",
        "token_id": "token"
    }


class CheckRequestHandleTests(TestCase):
    def test_handle_request_data_with_saturday_date_value(self):
        """
        A post request with a date to a saturday or sunday should return a json object like this:

        {
            "success": "false",
            "data": {},
            "error": {
                "code": 4,
                "message": "Cannot Schedule a meeting to a saturday or sunday."
            }
        }
        """
        register_user()
        response = self.client.post('/api/', get_json_object("2021", "16"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), "false")
        self.assertEqual(response.json().get('data'), {})
        self.assertEqual(response.json().get('error').get('code'), 4)
        self.assertEqual(response.json().get('error').get('message'),
                         'Cannot Schedule a meeting to a saturday or sunday.')

    def test_handle_request_data_with_past_date_value(self):
        """
        A post request with a past date should return a json object like this:

        {
            "success": "false",
            "data": {},
            "error": {
                "code": 5,
                "message": "Cannot Schedule a meeting to the past."
            }
        }
        """
        register_user()
        response = self.client.post('/api/', get_json_object("2006", "16"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), "false")
        self.assertEqual(response.json().get('data'), {})
        self.assertEqual(response.json().get('error').get('code'), 5)
        self.assertEqual(response.json().get('error').get('message'),
                         'Cannot Schedule a meeting to the past.')

    def test_handle_post_request_data_with_already_scheduled_value(self):
        """
        A post request with a date that is already scheduled should return a json object if the database_object.count
        value is smaller than 5

        {
            "success": "true",
            "data": {
                "date": "16-10-2065",
                "time": "16:30",
                "company-name": "Dr4kk0 Inc."
            },
            "error": {}
        }
        """
        register_user()
        response = self.client.post('/api/', get_json_object("2065", "16"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), "true")
        self.assertEqual(response.json().get('data').get('date'), "16-10-2065")
        self.assertEqual(response.json().get('data').get('time'), "16:30")
        self.assertEqual(response.json().get('data').get('company_name'), "Dr4kk0 Inc.")
        self.assertEqual(response.json().get('error'), {})

    def test_handle_post_request_data_with_five_scheduled_values_before_11_30(self):
        """
        5 post requests with a date that is already scheduled and the time is less than or equals 11:30 should return
        a json like this:

        {
            "success": "true",
            "data": {
                "date": "16-10-2065",
                "time": "10:30",
                "company-name": "Dr4kk0 Inc."
            },
            "error": {}
        }
        """

        register_user()

        for i in range(5):
            response = self.client.post('/api/', get_json_object("2065", "10"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('success'), "true")
            self.assertEqual(response.json().get('data').get('date'), "16-10-2065")
            self.assertEqual(response.json().get('data').get('time'), "10:30")
            self.assertEqual(response.json().get('data').get('company_name'), "Dr4kk0 Inc.")
            self.assertEqual(response.json().get('error'), {})

    def test_handle_post_request_data_with_five_scheduled_values_at_11_30(self):
        """
        5 post requests with a date that is already scheduled and the time is less than or equals 11:30 should return
        a json object like this:

        {
            "success": "true",
            "data": {
                "date": "16-10-2065",
                "time": "11:30",
                "company-name": "Dr4kk0 Inc."
            },
            "error": {}
        }
        """
        register_user()

        for i in range(5):
            response = self.client.post('/api/', get_json_object("2065", "11", "30"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('success'), "true")
            self.assertEqual(response.json().get('data').get('date'), "16-10-2065")
            self.assertEqual(response.json().get('data').get('time'), "11:30")
            self.assertEqual(response.json().get('data').get('company_name'), "Dr4kk0 Inc.")
            self.assertEqual(response.json().get('error'), {})

    def test_handle_post_request_data_with_three_scheduled_values_after_11_30(self):
        """
        3 post requests with a date that is already scheduled and the time is greater than 11:30 should return a json
        like this:

        {
            "success": "true",
            "data": {
                "date": "16-10-2065",
                "time": "12:30",
                "company-name": "Dr4kk0 Inc."
            },
            "error": {}
        }
        """
        register_user()

        for i in range(3):
            response = self.client.post('/api/', get_json_object("2065", "12"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('success'), "true")
            self.assertEqual(response.json().get('data').get('date'), "16-10-2065")
            self.assertEqual(response.json().get('data').get('time'), "12:30")
            self.assertEqual(response.json().get('data').get('company_name'), "Dr4kk0 Inc.")
            self.assertEqual(response.json().get('error'), {})

    def test_handle_post_request_data_with_five_scheduled_values_after_11_30(self):
        """"
        5 post requests with a date that is already scheduled and the time is greater than 11:30 should return a json
        like this:

        {
            "success": "false",
            data: {},
            error: {
                "code": 6,
                "message": "Number of meetings scheduled to the date and hour is over the allowed number."
            }
        }
        """
        register_user()

        for i in range(3):
            response = self.client.post('/api/', get_json_object("2065", "12"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('success'), "true")
            self.assertEqual(response.json().get('data').get('date'), "16-10-2065")
            self.assertEqual(response.json().get('data').get('time'), "12:30")
            self.assertEqual(response.json().get('data').get('company_name'), "Dr4kk0 Inc.")
            self.assertEqual(response.json().get('error'), {})

        response = self.client.post('/api/', get_json_object("2065", "12"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), "false")
        self.assertEqual(response.json().get('data'), {})
        self.assertEqual(response.json().get('error').get('code'), 6)
        self.assertEqual(response.json().get('error').get('message'),
                         'Number of meetings scheduled to the date and hour is over the allowed number.')

    def test_handle_post_request_data_with_six_scheduled_values(self):
        """
        6 post requests with a date that is already scheduled should return a json like this:

        {
            "success": "false",
            data: {},
            error: {
                "code": 6,
                "message": "Number of meetings scheduled to the date and hour is over the allowed number."
            }
        }
        """
        register_user()

        for i in range(5):
            response = self.client.post('/api/', get_json_object("2065", "10"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json().get('success'), "true")
            self.assertEqual(response.json().get('data').get('date'), "16-10-2065")
            self.assertEqual(response.json().get('data').get('time'), "10:30")
            self.assertEqual(response.json().get('data').get('company_name'), "Dr4kk0 Inc.")
            self.assertEqual(response.json().get('error'), {})

        response = self.client.post('/api/', get_json_object("2065", "10"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), "false")
        self.assertEqual(response.json().get('data'), {})
        self.assertEqual(response.json().get('error').get('code'), 6)
        self.assertEqual(response.json().get('error').get('message'),
                         'Number of meetings scheduled to the date and hour is over the allowed number.')


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

    new_user = User.objects.create(email='test@example.com', password='12345', token_id='token')
    new_scheduled_date.information_set.create(user=new_user)
    
    new_scheduled_date.save()
    scheduled_date_object = ScheduledDate.objects.get(date=datetime_object)

    return scheduled_date_object


# Requires creation
def update_scheduled_date():
    datetime_string = 'Oct 25 2066 16:20'
    datetime_object = datetime.strptime(datetime_string, '%b %d %Y %H:%M')

    new_scheduled_date = ScheduledDate.objects.select_for_update().get(date=datetime_object)
    new_scheduled_date.count += 1

    new_user = User.objects.create(email='test@example.com', password='12345', token_id='token')
    new_scheduled_date.information_set.create(user=new_user)
    
    new_scheduled_date.save()

    scheduled_date_object = ScheduledDate.objects.get(date=datetime_object)

    return scheduled_date_object


class CheckDatabaseHandleTests(TestCase):
    def test_handle_database_creation_with_no_existing_value(self):
        """
        Creating a new schedule when there is no existing object in the database should return true. Since the object
        was in fact created.
        """
        (scheduled_date_object, _) = create_scheduled_date()
        self.assertEqual(scheduled_date_object[1], True)

    def test_handle_database_creation_with_already_existing_value(self):
        """
        Creating a new schedule when there is already a existing schedule object in the database should return False,
        since the object is not brand new.
        """
        (first_object, _) = create_scheduled_date()
        (second_object, _) = create_scheduled_date()

        self.assertEqual(first_object[1], True)
        self.assertEqual(second_object[1], False)

    def test_handle_database_create_count_value(self):
        """
        Creating an object in the database with empty name and count, should create an object with default values:

        Name: 'Fake Business for tests only.'
        Count: 0
        """
        (_, scheduled_object) = create_scheduled_date()
        self.assertEqual(scheduled_object.count, 0)

    def test_handle_database_create_and_update_name_and_value(self):
        """
        Creating a new object in the database should set the count to 0.

        Adding a new object should increase the value to 1.

        Updating the name on the database should set the name to the updated name.
        """

        scheduled_date_object = create_and_update_scheduled_date()

        self.assertEqual(scheduled_date_object.count, 1)
        self.assertEqual(scheduled_date_object.information_set.all()[0].user.email, 'test@example.com')

    def test_handle_database_creating_5_schedules(self):
        """
        The database should be able to create 5 schedules to a same time.
        """
        (first_object, scheduled_date) = create_scheduled_date()

        self.assertEqual(first_object[1], True)
        self.assertEqual(scheduled_date.count, 0)

        for i in range(1, 5):
            scheduled_date = update_scheduled_date()
            self.assertEqual(scheduled_date.count, i)
