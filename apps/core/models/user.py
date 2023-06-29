from uuid import uuid4

from django.conf import settings
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


from ..mail import PasswordRecoveryEmailMessage
from ..managers import UserManager
from .profile import Profile


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
        profile (Profile): The profile data of the user.
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

        return self.profile.full_name

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
    def _profile_fields_names(cls):
        """Returns the fields names of the `Profile` model.

        Returns:
            list: The fields names of the `Profile` model.
        """

        if not hasattr(cls, '_profile_fields_names_cache'):
            cls._profile_fields_names_cache = [f.name for f in Profile._meta.fields
                                               if not f.primary_key and f.name != 'user']

        return cls._profile_fields_names_cache

    def _extract_profile_kwargs(self, kwargs):
        """Extracts the profile kwargs from the kwargs.

        Args:
            kwargs (dict): The kwargs to extract the profile kwargs from.

        Returns:
            dict: The kwargs without the profile kwargs.
        """

        profile_kwargs = {}
        for field in Profile._meta.fields:
            if any([field.name not in kwargs,
                    field.primary_key,
                    field.name == 'user']):
                continue

            profile_kwargs[field.name] = kwargs.pop(field.name)

        self.__dict__['_profile_attrs'] = profile_kwargs
        return kwargs

    def __init__(self, *args, **kwargs):
        kwargs = self._extract_profile_kwargs(kwargs)
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr_name):
        if attr_name not in self._profile_fields_names:
            return super().__getattribute__(attr_name)

        try:
            profile = super().__getattribute__('profile')
            return getattr(profile, attr_name)

        except Profile.DoesNotExist:
            if '_profile_attrs' in self.__dict__:
                return self.__dict__['_profile_attrs'][attr_name]

            else:
                return None

    def __setattr__(self, attr_name, value):
        if attr_name in self._profile_fields_names:
            if '_profile_attrs' not in self.__dict__:
                self.__dict__['_profile_attrs'] = {}

            self.__dict__['_profile_attrs'][attr_name] = value

        else:
            super().__setattr__(attr_name, value)

    def __str__(self) -> str:
        return f'{self.username} ({self.email})' if self.username else f'{self.email}'

    def clean(self):
        super().clean()

        if not self.email:
            error_msg = _('The email address is required.')
            raise exceptions.ValidationError({'email': error_msg})

        self.email = self._meta.model.objects.normalize_email(self.email)

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
            seconds=settings.PASSWORD_RECOVERY.get('TOKEN_TIMEOUT', (60*60*24))
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

    def get_password_recovery_email_message(self, **kwargs):
        """Gets the password reset email.

        Returns:
            PasswordResetEmailMessage: The password reset email.
        """

        message_kwargs = {
            'user': self
        }
        message_kwargs.update(kwargs)

        return PasswordRecoveryEmailMessage(**message_kwargs)
