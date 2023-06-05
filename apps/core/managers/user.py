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
            email_username = email.split('@')[0]
            kwargs['username'] = email_username

            while self.model.objects.filter(username=kwargs['username']).exists():
                timestamp_slice = str(int(datetime.now().timestamp()))[-5:]
                kwargs['username'] = f'{email_username}_{timestamp_slice}'

        person = kwargs.pop('person', {})

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        if person:
            for key, value in person.items():
                # NOTE `user.person` is guaranteed to exist because of the
                # `post_save` signal triggered by `User` creation.
                setattr(user.person, key, value)
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
