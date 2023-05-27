from django.contrib.auth import get_user_model


class UserTestsMixin:

    user = None

    def create_user(self, **kwargs):
        """Creates a new user.
        """

        user_kwargs = {
            'email': 'valid.email@test.com',
            'password': 'valid#password@123',
        }

        user_kwargs.update(kwargs)

        return get_user_model().objects.create_user(**user_kwargs)
