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
    @property
    def _person_fields_names(cls):
        """Returns the fields names of the `Person` model.

        Returns:
            list: The fields names of the `Person` model.
        """

        if not hasattr(cls, '_person_fields_names_cache'):
            cls._person_fields_names_cache = [f.name for f in Person._meta.fields
                                              if not f.primary_key and f.name != 'user']

        return cls._person_fields_names_cache

    def _extract_person_kwargs(self, kwargs):
        """Extracts the person kwargs from the kwargs.

        Args:
            kwargs (dict): The kwargs to extract the person kwargs from.

        Returns:
            dict: The kwargs without the person kwargs.
        """

        person_kwargs = {}
        for field in Person._meta.fields:
            if any([field.name not in kwargs,
                    field.primary_key,
                    field.name == 'user']):
                continue

            person_kwargs[field.name] = kwargs.pop(field.name)

        self.__dict__['_person_attrs'] = person_kwargs
        return kwargs

    def __init__(self, *args, **kwargs):
        kwargs = self._extract_person_kwargs(kwargs)
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr_name):
        if attr_name not in self._person_fields_names:
            return super().__getattribute__(attr_name)

        try:
            person = super().__getattribute__('person')
            return getattr(person, attr_name)

        except Person.DoesNotExist:
            if '_person_attrs' in self.__dict__:
                return self.__dict__['_person_attrs'][attr_name]

            else:
                return None

    def __setattr__(self, attr_name, value):
        if attr_name in self._person_fields_names:
            if '_person_attrs' not in self.__dict__:
                self.__dict__['_person_attrs'] = {}

            self.__dict__['_person_attrs'][attr_name] = value

        else:
            super().__setattr__(attr_name, value)

    def __str__(self) -> str:
        """Returns the string representation of the user.

        Returns the `username`, if set, followed by the `email`. Else returns
        just the `email`.

        Returns:
            str: The string representation of the user.
        """

        return f'{self.username} ({self.email})' if self.username else f'{self.email}'
