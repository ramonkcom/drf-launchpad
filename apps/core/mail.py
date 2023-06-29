from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from utils.helpers import load_entity


class CustomEmailMessage(EmailMultiAlternatives):
    """Utility class to help sending emails.

    This class is a wrapper around Django's `EmailMultiAlternatives` class.

    Attributes:
        html_body (str): The HTML body of the email.
    """

    html_body = None

    def __init__(self, *args, **kwargs):
        self.html_body = kwargs.pop('html_body', None)

        super().__init__(*args, **kwargs)

        # NOTE This is in case `get_body` is override in a subclass.
        if not self.body:
            self.body = self.get_body()

        # NOTE This is in case `get_html_body` is override in a subclass.
        if not self.html_body:
            self.html_body = self.get_html_body()

    def get_body(self):
        """Returns the body of the email as plain text.

        Returns:
            str: The body of the email as plain text.
        """

        return self.body

    def get_html_body(self):
        """Returns the body of the email as HTML.

        Returns:
            str: The body of the email as HTML.
        """

        return self.html_body

    def print(self):
        """Prints the email information to the console.
        """

        def join_recipients(recipients):
            return ', '.join([str(r) for r in recipients])

        print('\n\n', '='*80, sep='')
        print(f'SUBJECT: {self.subject}')
        print('-'*80)
        print(f'FROM: {self.from_email}')
        print(f'REPLY TO: {join_recipients(self.reply_to)}')
        print('-'*80)
        print(f'TO: {join_recipients(self.to)}')
        print(f'CC: {join_recipients(self.cc)}')
        print(f'BCC: {join_recipients(self.bcc)}')
        print('-'*80)
        print(self.get_body())
        print('='*80, '\n')

    def send(self, fail_silently=False, callback=None, send_in_dev=False):
        """Sends the email.

        Args:
            fail_silently (bool, optional): If `True`, exceptions will be
                silenced. Defaults to `False`.
            callback (function, optional): A function to be called to send
                the email instead of the default `send` method. Defaults to
                `None`.
            send_in_dev (bool, optional): If `True`, the email will be sent
                even if the `PRODUCTION` flag is `False`. Defaults to `False`.

        Returns:
            int: The number of emails sent.
        """

        if settings.TESTING:
            return 0

        if not settings.PRODUCTION and settings.DEBUG:
            self.print()

        if not settings.PRODUCTION and not send_in_dev:
            return 0

        if callable(callback):
            return callback()

        if self.html_body:
            self.attach_alternative(self.html_body, 'text/html')

        return super().send(fail_silently=fail_silently)


class VerificationEmailMessage(CustomEmailMessage):
    """Utility class to help sending verification emails.

    This class is a wrapper around Django's `EmailMultiAlternatives` class.

    Attributes:
        email_to_verify (Email): The email to be verified.
        html_body (str): The HTML body of the email.
    """

    email_to_verify = None

    def __init__(self, *args, **kwargs):
        from apps.core.models import Email
        self.email_to_verify = kwargs.pop('email_to_verify', None)

        if not self.email_to_verify:
            error_msg = _('A value for `email_to_verify` is required.')
            raise ValueError(error_msg)

        elif not isinstance(self.email_to_verify, Email):
            error_msg = _('`email_to_verify` must be an instance of `Email`.')
            raise ValueError(error_msg)

        super().__init__(*args, **kwargs)

        if not self.subject:
            self.subject = _('Verify your email address')

        self.to = [self.email_to_verify.address,]

    def get_body(self):
        copy = self.get_body_copy()

        return (
            f"{copy['title_text']}\n\n"
            f"{copy['main_text']}\n\n"
            f"Use the following link to confirm your email address:\n"
            f"{copy['confirmation_url']}\n\n"
            f"{copy['footer_text']}"
        )

    def get_body_copy(self):
        confirmation_base_url = settings.EMAIL_CONFIRMATION.get(
            'FRONTEND_BASE_URL', '')
        confirmation_params = {'id': self.email_to_verify.id,
                               'confirmation_code': self.email_to_verify.confirmation_code}
        confirmation_url = f'{confirmation_base_url}?{urlencode(confirmation_params)}'

        hours_to_expire = int(
            settings.EMAIL_CONFIRMATION.get('CODE_TIMEOUT', 3600) / 3600)

        default_copy = {
            'confirmation_url': confirmation_url,

            'title_text': _('Just one more step: verify your email address'),

            'main_text': _('Use the link below to verify this email address '
                           'on your account. If you prefer, you can also '
                           'copy and paste the link directly into your '
                           'browser. This link will expire in '
                           '%(n)s hours.') % {'n': hours_to_expire},

            'button_text': _('Verify email address'),

            'footer_text': _('If you did not create an account with this '
                             'email address, don\'t worry: you can safely '
                             'ignore this email.'),
        }

        return default_copy

    def get_html_body(self):
        copy = self.get_body_copy()

        return (
            f"<h1>{copy['title_text']}</h1>"
            f"<p>{copy['main_text']}</p>"
            f"<p><a href=\"{copy['confirmation_url']}\">{copy['button_text']}</a></p>"
            f"<p><em>Direct link: {copy['confirmation_url']}</em></p>"
            f"<p>{copy['footer_text']}</p>"
        )

    def print(self):
        super().print()

        if settings.DEBUG:
            from django.urls import reverse

            backend_data = {'confirmation_code': str(
                self.email_to_verify.confirmation_code)}
            backend_url = (
                reverse('core:email-confirmation', args=[self.email_to_verify.pk]))

            print('='*80)
            print('DEBUG INFO:')
            print('-'*80)
            print(f'Email ID: {self.email_to_verify.id}')
            print(f'Email Address: {self.email_to_verify.address}')
            print(
                f'Confirmation Code: {self.email_to_verify.confirmation_code}')
            print(f'Backend URL: {backend_url}')
            print(f'Backend Payload Data: {backend_data}')
            print('='*80, '\n')

    def send(self, fail_silently=False):
        callback = None
        if callback_path := settings.EMAIL_CONFIRMATION.get('SEND_EMAIL_CALLBACK', None):
            send_callback = load_entity(callback_path)

            def callback(): return send_callback(self)

        send_in_dev = settings.EMAIL_CONFIRMATION.get(
            'SEND_EMAIL_IN_DEV', False)

        return super().send(fail_silently=fail_silently,
                            callback=callback,
                            send_in_dev=send_in_dev)


class PasswordRecoveryEmailMessage(CustomEmailMessage):
    """Utility class to help sending password recovery emails.

    This class is a wrapper around Django's `EmailMultiAlternatives` class.

    Attributes:
        html_body (str): The HTML body of the email.
        user (User): The user to recover the password.
    """

    user = None

    def __init__(self, *args, **kwargs):
        from apps.core.models import User
        self.user = kwargs.pop('user', None)

        if not self.user:
            error_msg = _('A value for `user` is required.')
            raise ValueError(error_msg)

        elif not isinstance(self.user, User):
            error_msg = _('`user` must be an instance of `User`.')
            raise ValueError(error_msg)

        super().__init__(*args, **kwargs)

        if not self.subject:
            self.subject = _('Reset your password')

        self.to = [self.user.email,]

    def get_body(self):
        copy = self.get_body_copy()

        return (
            f"{copy['title_text']}\n\n"
            f"{copy['main_text']}\n\n"
            f"Use the following link to reset your password:\n"
            f"{copy['password_reset_url']}\n\n"
            f"{copy['footer_text']}"
        )

    def get_body_copy(self):
        password_reset_base_url = settings.PASSWORD_RECOVERY.get(
            'FRONTEND_BASE_URL', '')
        password_reset_params = {'id': self.user.id,
                                 'reset_token': self.user.reset_token}
        password_reset_url = f'{password_reset_base_url}?{urlencode(password_reset_params)}'

        hours_to_expire = int(
            settings.PASSWORD_RECOVERY.get('TOKEN_TIMEOUT', 3600) / 3600)

        default_copy = {
            'password_reset_url': password_reset_url,

            'title_text': _('Set a new password'),

            'main_text': _('Use the link below to set a new password '
                           'for your account. If you prefer, you can also '
                           'copy and paste the link directly into your '
                           'browser. This link will expire in '
                           '%(n)s hours.') % {'n': hours_to_expire},

            'button_text': _('Reset password'),

            'footer_text': _('If you did not ask for a password reset, don\'t '
                             'worry: you can safely ignore this email.'),
        }

        return default_copy

    def get_html_body(self):
        copy = self.get_body_copy()

        return (
            f"<h1>{copy['title_text']}</h1>"
            f"<p>{copy['main_text']}</p>"
            f"<p><a href=\"{copy['password_reset_url']}\">{copy['button_text']}</a></p>"
            f"<p><em>Direct link: {copy['password_reset_url']}</em></p>"
            f"<p>{copy['footer_text']}</p>"
        )

    def print(self):
        super().print()

        if settings.DEBUG:
            from django.urls import reverse

            backend_data = {'user_id': self.user.id,
                            'reset_token': str(self.user.reset_token),
                            'password_1': 'NEW_PASSWORD',
                            'password_2': 'NEW_PASSWORD', }
            backend_url = reverse('core:password-reset')

            print('='*80)
            print('DEBUG INFO:')
            print('-'*80)
            print(f'User ID: {self.user.id}')
            print(f'Reset Token: {self.user.reset_token}')
            print(f'Backend URL: {backend_url}')
            print(f'Backend Payload Data: {backend_data}')
            print('='*80, '\n')

    def send(self, fail_silently=False):
        callback = None
        if callback_path := settings.PASSWORD_RECOVERY.get('SEND_EMAIL_CALLBACK', None):
            send_callback = load_entity(callback_path)

            def callback(): return send_callback(self)

        send_in_dev = settings.PASSWORD_RECOVERY.get(
            'SEND_EMAIL_IN_DEV', False)

        return super().send(fail_silently=fail_silently,
                            callback=callback,
                            send_in_dev=send_in_dev)
