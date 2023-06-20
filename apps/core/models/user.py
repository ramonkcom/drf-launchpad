from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core import (
    exceptions,
    validators,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.mail import PasswordResetEmailMessage

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
        reset_token (str): The token to reset the password of the user.
        reset_token_date (datetime): The date the reset token was generated.
        user_permissions (Manager<Permission>): The permissions of the user.
        username (str): The username of the user.
    """

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email',]

    objects = UserManager()

    USERNAME_FIELD = 'email'

    RESET_TOKEN_TIMEOUT = 60 * 60 * 24

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

    reset_token = models.UUIDField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_('reset token'),
    )

    reset_token_date = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_('reset token date'),
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

    @classmethod
    @property
    def factory(cls):
        """Returns the factory for the `User` model.

        Returns:
            UserFactory: The factory for the `User` model.
        """

        from ..factories import UserFactory
        return UserFactory

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
        return f'{self.username} ({self.email})' if self.username else f'{self.email}'

    def clean(self):
        super().clean()

        if not self.email:
            error_msg = _('Email address is required.')
            raise exceptions.ValidationError({'email': error_msg})

        self.email = self._meta.model.objects.normalize_email(self.email)

        if (self.is_superuser or self.is_staff) and not self.password:
            error_msg = _('Password is required.')
            raise exceptions.ValidationError({'password': error_msg})

    def clear_reset_token(self, save=False):
        """Clears the reset token of the user.

        Args:
            save (bool): Whether to save the user or not.
        """

        self.reset_token = None
        self.reset_token_date = None

        if save:
            self.save()

    def check_reset_token(self, reset_token):
        """Checks if the reset token is valid.

        Args:
            reset_token (str): The reset token to be checked.

        Returns:
            bool: Whether the reset token is valid or not.
        """

        if not self.reset_token:
            return False

        expiration_date = self.reset_token_date + timezone.timedelta(
            seconds=self.RESET_TOKEN_TIMEOUT
        )

        return all([
            str(self.reset_token) == reset_token,
            timezone.now() < expiration_date
        ])

    def generate_reset_token(self, overwrite=True, save=False):
        """Generates a new reset token for the user.

        Args:
            overwrite (bool): Whether to overwrite the current reset token or not.
            save (bool): Whether to save the user or not.

        Returns:
            str: The reset token.
        """

        if overwrite or not self.reset_token:
            self.reset_token = uuid4()
            self.reset_token_date = timezone.now()

        if save:
            self.save()

        return self.reset_token

    def get_password_reset_email(self, **kwargs):
        """Gets the password reset email.

        Returns:
            PasswordResetEmailMessage: The password reset email.
        """

        message_kwargs = {
            'user': self
        }
        message_kwargs.update(kwargs)

        return PasswordResetEmailMessage(**message_kwargs)
