from datetime import datetime

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for the `User` model.
    """

    def create_user(self, email, password=None, **kwargs):
        """Creates, saves and returns a new user.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password. Defaults to `None`.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            User: The created user.
        """

        if not email:
            error_msg = _('Email address is required.')
            raise ValueError(error_msg)

        kwargs['username'] = kwargs.pop('username', None)

        if not kwargs['username']:
            kwargs['username'] = email.split(
                '@')[0] + '_' + str(int(datetime.now().timestamp()))[-5:]

        given_name = kwargs.pop('given_name', 'Superuser')
        family_name = kwargs.pop('family_name', 'Django')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        # NOTE `user.person` is guaranteed to exist because of the `post_save`
        # signal triggered by `User` creation.
        user.person.given_name = given_name
        user.person.family_name = family_name
        user.person.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """Creates, saves and returns a superuser.

        Args:
            email (str): The superuser's email address.
            password (str): The superuser's password.

        Returns:
            User: The superuser created.
        """

        superuser = self.create_user(email=email,
                                     password=password,
                                     **kwargs)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

        return superuser
