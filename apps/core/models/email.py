import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Email(models.Model):
    """Represents an user email.

    Attributes:
        address (str): The email address.
        confirmation_code (UUID): The confirmation code.
        confirmation_code_date (datetime): The date the confirmation code
            was generated. Defaults to now.
        confirmation_date (datetime): The confirmation date.
        origin (str): The origin of the email. Defaults to `USER_INPUT`.
        user (User): The user related to the email.
    """

    class Meta:
        verbose_name = _('email')
        verbose_name_plural = _('emails')
        ordering = ['address',]

    class Origin(models.TextChoices):
        """Origin of the email.
        """

        DEFAULT_SIGNUP = 'DEFAULT_SIGNUP', _('Default Sign Up')
        USER_INPUT = 'USER_INPUT', _('User Input')

    CONFIRMATION_CODE_TIMEOUT = 60 * 60 * 24

    # ---------------------------------- FIELDS ---------------------------------- #

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    address = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'),
    )

    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('confirmation code'),
    )

    confirmation_code_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('confirmation code date'),
    )

    confirmation_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('confirmation date'),
    )

    origin = models.CharField(
        max_length=255,
        choices=Origin.choices,
        default=Origin.USER_INPUT,
        verbose_name=_('origin'),
    )

    user = models.ForeignKey(
        to='core.User',
        on_delete=models.CASCADE,
        related_name='emails',
        verbose_name=_('user'),
    )

    # -------------------------------- PROPERTIES -------------------------------- #

    @property
    def is_confirmed(self):
        """Whether the email is confirmed or not.

        Returns:
            bool: Whether the email is confirmed or not.
        """

        return self.confirmation_date is not None

    @property
    def is_primary(self):
        """Whether the email is primary or not.

        Returns:
            bool: Whether the email is primary or not.
        """

        return self.address == self.user.email

    # ---------------------------------- METHODS --------------------------------- #

    def __str__(self):
        return str(self.address)

    def confirm(self):
        """Confirms the email, setting the confirmation date to now.
        """

        self.confirmation_date = timezone.now()
        self.save()

    def check_confirmation_code(self, confirmation_code):
        """Checks if the confirmation code is valid.

        Args:
            confirmation_code (UUID): The confirmation code to be checked.

        Returns:
            bool: Whether the confirmation code is valid or not.
        """

        expiration_date = self.confirmation_code_date + timezone.timedelta(
            seconds=self.CONFIRMATION_CODE_TIMEOUT
        )

        return all([
            str(self.confirmation_code) == confirmation_code,
            timezone.now() < expiration_date
        ])

    def regenerate_confirmation_code(self):
        """Regenerates the confirmation code.

        Returns:
            UUID: The new confirmation code.
        """

        self.confirmation_code = uuid.uuid4()
        self.confirmation_code_date = timezone.now()
