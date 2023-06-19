from django.utils.translation import gettext_lazy as _

from ...models import User
from ...factories import UserFactory


class UserTestMixin:

    user = None

    def build_user(self, **kwargs):
        """Builds a new user, without saving it to the DB.

        Returns:
            User: The new user.
        """

        password = kwargs.pop('password', '')

        user = UserFactory.build(**kwargs)

        if password != '':
            user.set_password(password)

        return user

    def create_user(self, **kwargs):
        """Creates a new user.

        Returns:
            User: The new user.
        """

        user_dict = UserFactory.build_dict(**kwargs)
        return User.objects.create_user(**user_dict)

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
