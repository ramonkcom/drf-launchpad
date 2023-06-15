from typing import Any
from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from .person import Person
from ..managers import UserManager


class User(AbstractBaseUser,
           PermissionsMixin):
    """Represents an user in the system.

    Attributes:
        id (uuid): The unique identifier of the user.
        date_joined (datetime): The date the user joined the system.
        email (str): The primary email of the user.
        emails (Manager<Email>): Emails of the user.
        groups (Manager<Group>): The permission groups of the user.
        is_active (bool): Whether the user is active or not.
        is_staff (bool): Whether the user is staff or not.
        is_superuser (bool): Whether the user is superuser or not.
        last_login (datetime): The last login of the user.
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

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date joined"),
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
            '31 characters or fewer. Letters, digits and ./_ only.'
        ),
        validators=[validators.RegexValidator(
            regex=r"^[\w](?!.*?\.{2})[\w.]{1,29}[\w]$"
        ),],
        error_messages={
            'unique': _('An user with that username already exists.'),
        },
    )

    # -------------------------------- PROPERTIES -------------------------------- #

    @property
    def full_name(self) -> str:
        """Returns the full name of the user.

        Returns:
            str: The full name of the user.
        """

        return self.person.full_name

    @property
    def is_anonymous(self):
        """Returns whether the user is anonymous or not.

        Returns:
            bool: Whether the user is anonymous or not.
        """

        from django.conf import settings

        return self.username == settings.ANONYMOUS_USER_NAME

    @property
    def primary_email(self):
        """Returns the primary email of the user.

        Returns:
            Email: The primary email of the user.
        """

        return self.emails.filter(address=self.email).first()

    # ---------------------------------- METHODS --------------------------------- #

    @classmethod
    def _extract_person_kwargs(cls, kwargs):
        """Extracts the person kwargs from the kwargs.

        Args:
            kwargs (dict): The kwargs to extract the person kwargs from.

        Returns:
            tuple[dict, dict]: The kwargs without the person kwargs, and the
                person kwargs.
        """

        person_kwargs = {}
        for field in Person._meta.fields:
            if field.name not in kwargs or field.primary_key or field.related_model:
                continue

            person_kwargs[field.name] = kwargs.pop(field.name)

        return kwargs, person_kwargs

    def __init__(self, *args, **kwargs):
        kwargs, person_kwargs = self._extract_person_kwargs(kwargs)

        super().__init__(*args, **kwargs)

        try:
            getattr(self, 'person')

        except Person.DoesNotExist:
            person_kwargs['user_id'] = self.id
            self.person = Person(**person_kwargs)

    def __getattr__(self, attr_name):
        person = super().__getattribute__('person')

        if not person:
            return super().__getattribute__(attr_name)

        person_fields = [f.name for f in Person._meta.fields
                         if not f.primary_key and not f.related_model]

        if attr_name in person_fields:
            return getattr(person, attr_name)

        return super().__getattribute__(attr_name)

    def __setattr__(self, attr_name, value):
        person_fields = [f.name for f in Person._meta.fields
                         if not f.primary_key and not f.related_model]

        if attr_name in person_fields:
            setattr(self.person, attr_name, value)

        super().__setattr__(attr_name, value)

    def __str__(self) -> str:
        """Returns the string representation of the user.

        Returns the `username`, if set, followed by the `email`. Else returns
        just the `email`.

        Returns:
            str: The string representation of the user.
        """

        return f'{self.username} ({self.email})' if self.username else f'{self.email}'
