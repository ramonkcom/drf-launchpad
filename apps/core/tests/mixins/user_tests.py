from datetime import datetime

from django.contrib.auth import get_user_model


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
