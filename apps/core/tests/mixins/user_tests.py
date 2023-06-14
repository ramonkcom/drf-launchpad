from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


class UserTestsMixin:

    user = None

    def create_user(self, **kwargs):
        """Creates a new user.

        If not provided, the following kwargs will be used:
            - email: 'valid.email@test.com'
            - password: 'valid#password@123'

        Returns:
            User: The new user.
        """

        user_kwargs = {
            'email': 'valid.email@test.com',
            'password': 'valid#password@123',
        }
        user_kwargs.update(kwargs)

        email_username = user_kwargs['email'].split('@', maxsplit=1)[0]
        kwargs['username'] = email_username

        while get_user_model().objects.filter(username=kwargs['username']).exists():
            timestamp_slice = str(int(datetime.now().timestamp()))[-5:]
            kwargs['username'] = f'{email_username}_{timestamp_slice}'

        return get_user_model().objects.create_user(**user_kwargs)


class UserAPITestsMixin(UserTestsMixin):

    api_client = None

    def setUp(self):  # pylint: disable=invalid-name
        self.api_client = self.create_api_client()

    def create_api_client(self, auth_user=None, **kwargs):
        """Creates and returns an API client.

        Args:
            auth_user (User, optional): The user to authenticate.

        Returns:
            APIClient: The new API client.
        """

        api_client = APIClient()

        if auth_user:
            api_client.force_authenticate(user=auth_user)

        return api_client

    def authenticate(self, user, api_client=None, **kwargs):
        """Authenticates an user by force.

        Args:
            user (User): The user to be authenticated.
            api_client (APIClient, optional): The API client to be used.

        Returns:
            User: The authenticated user.
        """

        api_client = self.api_client if not api_client else api_client
        api_client.force_authenticate(user=user)
        return user

    def create_user_payload(self, **kwargs):
        """Creates valid user payload data.

        If no kwargs are provided, the following kwargs will be used:
            - given_name: 'Valid'
            - family_name: 'User'
            - email: 'valid.email@test.com'
            - password_1: 'valid#pass!123'
            - password_2: 'valid#pass!123'

        If only `update=True` is provided, the following kwargs will be used:
            - given_name: 'Valid Updated'
            - family_name: 'User Updated'
            - password_1: 'NEW_valid#pass!123'
            - password_2: 'NEW_valid#pass!123'

        Returns:
            dict: The user payload data.
        """

        update = kwargs.pop('update', False)

        data = {
            'given_name': 'Valid',
            'family_name': 'User',
            'email': 'valid.email@test.com',
            'password_1': 'valid#pass!123',
            'password_2': 'valid#pass!123',
        }

        if update:
            data = {
                'given_name': 'Valid Updated',
                'family_name': 'User Updated',
                'password_1': 'NEW_valid#pass!123',
                'password_2': 'NEW_valid#pass!123',
            }

        data.update(kwargs)
        return data
