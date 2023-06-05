from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core import validators

from ..managers import UserManager


class User(AbstractBaseUser,
           PermissionsMixin):
    """Represents an user in the system.

    Attributes:
        id (uuid): The unique identifier of the user.
        email (str): The email of the user.
        given_name (str): The given name of the user.
        groups (Manager<Group>): The permission groups of the user.
        family_name (str): The family name of the user.
        is_active (bool): Whether the user is active or not.
        is_staff (bool): Whether the user is staff or not.
        is_superuser (bool): Whether the user is superuser or not.
        person (Person): The person related to the user.
        user_permissions (Manager<Permission>): The permissions of the user.
        username (str): The username of the user.
    """

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email',]

    objects = UserManager()

    USERNAME_FIELD = 'email'

    # ---------------------------------- FIELDS ---------------------------------- #

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active?'),
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is staff?'),
    )

    username = models.CharField(
        verbose_name=_("username"),
        max_length=31,
        null=True,
        blank=True,
        unique=True,
        help_text=_(
            'Required. 31 characters or fewer. Letters, digits and ./_ only.'
        ),
        validators=[validators.RegexValidator(
            regex=r"^[\w](?!.*?\.{2})[\w.]{1,29}[\w]$"
        ),],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )

    # -------------------------------- PROPERTIES -------------------------------- #

    @property
    def given_name(self) -> str:
        """Returns the given name of the person.

        Returns:
            str: The given name of the person.
        """

        return self.person.given_name

    @property
    def family_name(self) -> str:
        """Returns the family name of the person.

        Returns:
            str: The family name of the person.
        """

        return self.person.family_name

    @property
    def full_name(self) -> str:
        """Returns the full name of the person.

        Returns:
            str: The full name of the person.
        """

        return self.person.full_name

    # ---------------------------------- METHODS --------------------------------- #

    def __str__(self) -> str:
        """Returns the string representation of the user.

        Returns the `username`, if set, followed by the `email`. Else returns
        just the `email`.

        Returns:
            str: The string representation of the user.
        """

        return f'{self.username} ({self.email})' if self.username else f'{self.email}'
