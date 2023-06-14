import uuid

from django.conf import settings
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

    def get_verification_email(self, **kwargs):
        """Gets the verification email.

        Returns:
            VerificationEmail: The verification email.
        """

        message_kwargs = {
            'email': self
        }
        message_kwargs.update(kwargs)

        return VerificationEmail(**message_kwargs)

    def regenerate_confirmation_code(self):
        """Regenerates the confirmation code.

        Returns:
            UUID: The new confirmation code.
        """

        self.confirmation_code = uuid.uuid4()
        self.confirmation_code_date = timezone.now()


class VerificationEmail:
    """Utility class to help sending verification emails.

    Attributes:
        email (Email): the email to be confirmed.
        confirmation_base_url (str): the frontend URL to confirm emails,
            without parameters.
        title_text (str): the text to be used as the title.
        body_text (str): the text to be used as the body.
        button_text (str): the text to be used as the confirmation button
            label.
        footer_text (str): the text to be used as the footer.
    """

    def __init__(self, **kwargs):
        self.email = kwargs.get('email', None)

        if not self.email:
            error_msg = _('A value for `email` is required.')
            raise ValueError(error_msg)

        defaults = {
            'confirmation_base_url': 'https://FRONTEND_URL/CONFIRM_EMAIL_PATH/',

            'title_text': _('Just one more step: verify your email address.'),

            'body_text': _('Use the link below to verify this email address '
                           'on your account. If you prefer, you can also '
                           'copy and paste the link below into your browser. '
                           'This link will expire in 24 hours.'),

            'button_text': _('Verify email address'),

            'footer_text': _('If you did not create an account with this '
                             'email address, don\'t worry: you can safely '
                             'ignore this email.'),
        }

        for attr_name, default_value in defaults.items():
            setattr(self, attr_name, kwargs.get(attr_name, default_value))

    def get_confirmation_url(self):
        """Returns the confirmation URL.
        """

        from django.utils.http import urlencode

        confirmation_params = {'id': self.email.id,
                               'confirmation_code': self.email.confirmation_code}
        return f'{self.confirmation_base_url}?{urlencode(confirmation_params)}'

    def get_html(self):
        """Returns the HTML version of the verification email content.
        """

        confirmation_url = self.get_confirmation_url()
        return (
            f'<h1>{self.title_text}</h1>'
            f'<p>{self.body_text}</p>'
            f'<p><a href="{confirmation_url}">{self.button_text}</a></p>'
            f'<p><em>Direct link: {confirmation_url}</em></p>'
            f'<p>{self.footer_text}</p>'
        )

    def get_plain_text(self):
        """Returns the plain text version of the verification email content.
        """

        confirmation_url = self.get_confirmation_url()
        return (
            f'{self.title_text}\n\n'
            f'{self.body_text}\n\n'
            f'Use the following link to confirm your email address:\n'
            f'{confirmation_url}\n\n'
            f'{self.footer_text}'
        )

    def send(self):
        """Sends the verification email.
        """

        if settings.TESTING:
            return

        if settings.DEBUG:
            return self.print()

        # Plug the code to send email confirmation here.
        error_msg = _('You must provide a `send` implementation.')
        raise NotImplementedError(error_msg)

    def print(self):
        """Prints the verification email to the console.
        """

        print('\n\n', '='*80, sep='')
        print('VERIFICATION EMAIL:')
        print('-'*80)
        print(self.get_plain_text())
        print('='*80, '\n')

        if settings.DEBUG:
            from django.urls import reverse

            backend_data = {'confirmation_code': str(
                self.email.confirmation_code)}
            backend_url = (
                reverse('core:email-confirmation', args=[self.email.pk]))

            print('='*80)
            print('DEBUG INFO:')
            print('-'*80)
            print(f'Email ID: {self.email.id}')
            print(f'Email Address: {self.email.address}')
            print(f'Confirmation Code: {self.email.confirmation_code}')
            print(f'Backend URL: {backend_url}')
            print(f'Backend Payload Data: {backend_data}')
            print('='*80, '\n')
