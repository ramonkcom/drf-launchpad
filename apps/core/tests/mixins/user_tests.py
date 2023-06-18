from rest_framework.test import APIClient

from ...models import User
from ...factories import UserFactory


class UserTestsMixin:

    user = None

    def create_user(self, **kwargs):
        """Creates a new user.

        Returns:
            User: The new user.
        """

        user_dict = UserFactory.build_dict(**kwargs)
        return User.objects.create_user(**user_dict)

    def build_user(self, **kwargs):
        """Builds a new user.

        Returns:
            User: The new user.
        """

        password = kwargs.pop('password', '')

        user = UserFactory.build(**kwargs)

        if password != '':
            user.set_password(password)

        return user


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

        Returns:
            dict: The user payload data.
        """

        exclude_fields = kwargs.pop('exclude_fields', [])
        include_fields = kwargs.pop('include_fields', [])

        exclude_fields.extend([f for f in [
            'is_active',
            'is_staff',
            'is_superuser',
        ] if f not in include_fields])

        user_dict = UserFactory.build_dict(include_fields=include_fields,
                                           exclude_fields=exclude_fields,
                                           **kwargs)
        password = user_dict.pop('password', '')

        if password != '' and 'password_1' not in user_dict and 'password_2' not in user_dict:
            user_dict['password_1'] = password
            user_dict['password_2'] = password

        return user_dict
