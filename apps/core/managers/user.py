from datetime import datetime

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for the `User` model.
    """

    def create_user(self, email, **kwargs):
        """Creates, saves and returns a new user.

        Args:
            email (str): The user's email address.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            User: The created user.
        """

        if not email:
            error_msg = _('Email address is required.')
            raise ValueError(error_msg)

        if 'username' not in kwargs:
            email_username = email.split('@')[0]
            kwargs['username'] = email_username

            while self.model.objects.filter(username=kwargs['username']).exists():
                timestamp_slice = str(int(datetime.now().timestamp()))[-5:]
                kwargs['username'] = f'{email_username}_{timestamp_slice}'

        password = kwargs.pop('password', None)
        user = self.model(email=self.normalize_email(email), **kwargs)

        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """Creates, saves and returns a superuser.

        Args:
            email (str): The superuser's email address.
            password (str): The superuser's password.

        Returns:
            User: The superuser created.
        """

        if not email:
            error_msg = _('Email address is required.')
            raise ValueError(error_msg)

        if not password:
            error_msg = _('Password is required.')
            raise ValueError(error_msg)

        superuser = self.create_user(email=email,
                                     password=password,
                                     is_staff=True,
                                     is_superuser=True,
                                     **kwargs)
        superuser.save()
        return superuser
