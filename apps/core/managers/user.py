from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, **kwargs):
        """Creates, saves and returns a new user.

        Args:
            email (str): The user's email address.

        Returns:
            User: The created user.
        """

        password = kwargs.pop('password', None)

        user = self.model(email=email, **kwargs)
        user.clean()

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

        superuser = self.create_user(email=email,
                                     password=password,
                                     is_staff=True,
                                     is_superuser=True,
                                     **kwargs)
        return superuser
