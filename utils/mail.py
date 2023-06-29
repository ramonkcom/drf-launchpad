import re

from django.conf import settings
from django.utils.translation import gettext_lazy as _


class EmailMessage:
    """Utility class to help sending emails.

    Attributes:
        bcc (list[tuple(str, str)]): the list of BCC recipients as tuples,
            containing the email address and the name of the recipient.
        cc (list[tuple(str, str)]): the list of CC recipients as tuples,
            containing the email address and the name of the recipient.
        footer_text (str): the text to be used as the footer.
        main_text (str): the text to be used as the body.
        sender (tuple, optional): the sender as a tuple containing the
            email address and the name of the sender. Defaults to the value of
            `settings.DEFAULT_FROM_EMAIL`.
        subject (str): the subject of the email.
        title_text (str): the text to be used as the title.
        to (list[tuple(str, str)]): the list of recipients as tuples,
            containing the email address and the name of the recipient.
    """

    bcc = None
    cc = None
    footer_text = None
    main_text = None
    sender = None
    subject = None
    title_text = None
    to = None

    def validate_recipients(self, recipients_label, recipients):
        error_msg = _(
            '`%(arg)s` must be a list of tuples '
            '(e.g. [("recipient@example.com", "Recipient"),])'
        ) % {'arg': recipients_label}

        if not isinstance(recipients, list):
            raise ValueError(error_msg)

        else:
            for tuple_item in recipients:
                if not isinstance(tuple_item, tuple):
                    raise ValueError(error_msg)

                email_regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
                email_address = str(tuple_item[0])
                if not re.match(email_regex, email_address):
                    error_msg = _('%(email)s is not a valid email address.') % {
                        'email': email_address}
                    raise ValueError(error_msg)

    def __init__(self, **kwargs):
        self.bcc = []
        self.cc = []
        self.to = []

        if 'sender' not in kwargs:
            kwargs['sender'] = settings.EMAIL_CONFIRMATION.get(
                'DEFAULT_FROM', None)

        for key, value in kwargs.items():
            if key in ['bcc', 'cc', 'to']:
                self.validate_recipients(key, value)
                setattr(self, key, value)

            elif key == 'sender':
                if not isinstance(kwargs['sender'], tuple):
                    error_msg = _('`sender` must be a tuple '
                                  '(e.g. ("noreply@example.com", "Sender"))')
                    raise ValueError(error_msg)

                email_regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
                email_address = str(kwargs['sender'][0])
                if not re.match(email_regex, email_address):
                    error_msg = _('%(email)s is not a valid email address.') % {
                        'email': email_address}
                    raise ValueError(error_msg)

                setattr(self, key, value)

            elif hasattr(self, key):
                setattr(self, key, str(value))

    def get_html_body(self):
        """Returns the HTML version of the email content.
        """

        return (
            f'<h1>{self.title_text}</h1>'
            f'<p>{self.main_text}</p>'
            f'<p>{self.footer_text}</p>'
        )

    def get_plain_text_body(self):
        """Returns the plain text version of the email content.
        """

        return (
            f'{self.title_text}\n\n'
            f'{self.main_text}\n\n'
            f'{self.footer_text}'
        )

    def get_send_callback(self, callback_name):
        """Returns the callback function to send the email.

        Args:
            callback_name (str): the name of the callback function.

        Returns:
            function: the callback function.
        """

        import importlib

        module_name, function_name = callback_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, function_name)

    def print(self):
        """Prints the email to the console.
        """

        def format_recipients(recipients):
            return ', '.join([f'{name} <{email}>' for email, name in recipients])

        print('\n\n', '='*80, sep='')
        print(f'SUBJECT: {self.subject}')
        print(f'TO: {format_recipients(self.to)}')
        print(f'CC: {format_recipients(self.cc)}')
        print(f'BCC: {format_recipients(self.bcc)}')
        print('-'*80)
        print(self.get_plain_text_body())
        print('='*80, '\n')

    def send(self):
        """Sends the email.
        """

        import warnings

        if settings.TESTING:
            return

        if settings.DEBUG:
            return self.print()

        if settings.PRODUCTION:
            # Plug the code to send email confirmation here.
            error_msg = _('You must provide a `send` implementation.')
            raise NotImplementedError(error_msg)

        else:
            warn_msg = str(_('Notice: `send` not implemented.'))
            warnings.warn(warn_msg)


class VerificationEmailMessage(EmailMessage):
    """Utility class to help sending verification emails.

    Attributes:
        bcc (list[tuple(str, str)]): the list of BCC recipients as tuples,
            containing the email address and the name of the recipient.
        button_text (str): the text to be used as the button.
        cc (list[tuple(str, str)]): the list of CC recipients as tuples,
            containing the email address and the name of the recipient.
        confirmation_base_url (str): the base URL (without parameters) to be
            used on the confirmation link.
        email (Email): the email to be verified.
        footer_text (str): the text to be used as the footer.
        main_text (str): the text to be used as the body.
        subject (str): the subject of the email.
        title_text (str): the text to be used as the title.
    """

    button_text = None
    confirmation_base_url = None

    def __init__(self, **kwargs):
        from apps.core.models import Email
        self.email = kwargs.get('email', None)

        if not self.email:
            error_msg = _('A value for `email` is required.')
            raise ValueError(error_msg)

        elif not isinstance(self.email, Email):
            error_msg = _('`email` must be an instance of `Email`.')
            raise ValueError(error_msg)

        super_kwargs = {
            'to': [(self.email.address, self.email.user.full_name),], }

        hours_to_expire = int(
            settings.EMAIL_CONFIRMATION['CODE_TIMEOUT'] / 3600)

        defaults = {
            'confirmation_base_url': 'https://FRONTEND_URL/CONFIRM_EMAIL_PATH/',

            'subject': _('Verify your email address'),

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

        for attr_name, default_value in defaults.items():
            super_kwargs[attr_name] = kwargs.get(attr_name, default_value)

        super().__init__(**super_kwargs)

    def get_confirmation_url(self):
        """Returns the confirmation URL.
        """

        from django.utils.http import urlencode

        confirmation_params = {'id': self.email.id,
                               'confirmation_code': self.email.confirmation_code}
        return f'{self.confirmation_base_url}?{urlencode(confirmation_params)}'

    def get_html_body(self):
        """Returns the HTML version of the verification email content.
        """

        confirmation_url = self.get_confirmation_url()
        return (
            f'<h1>{self.title_text}</h1>'
            f'<p>{self.main_text}</p>'
            f'<p><a href="{confirmation_url}">{self.button_text}</a></p>'
            f'<p><em>Direct link: {confirmation_url}</em></p>'
            f'<p>{self.footer_text}</p>'
        )

    def get_plain_text_body(self):
        """Returns the plain text version of the verification email content.
        """

        confirmation_url = self.get_confirmation_url()
        return (
            f'{self.title_text}\n\n'
            f'{self.main_text}\n\n'
            f'Use the following link to confirm your email address:\n'
            f'{confirmation_url}\n\n'
            f'{self.footer_text}'
        )

    def print(self):
        """Prints the verification email to the console.
        """

        super().print()

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

    def send(self):
        if ('SEND_EMAIL_CALLBACK' not in settings.EMAIL_CONFIRMATION
                or not settings.EMAIL_CONFIRMATION['SEND_EMAIL_CALLBACK']):
            return super().send()

        callback_name = settings.EMAIL_CONFIRMATION['SEND_EMAIL_CALLBACK']
        send_confirmation_email = self.get_send_callback(callback_name)
        return send_confirmation_email(subject=self.subject,
                                       plain_text=self.get_plain_text_body(),
                                       html=self.get_html_body(),
                                       sender=self.sender,
                                       to=self.to,
                                       cc=self.cc,
                                       bcc=self.bcc,
                                       email_instance=self.email)


class PasswordResetEmailMessage(EmailMessage):
    """Utility class to help sending password reset emails.

    Attributes:
        bcc (list[tuple(str, str)]): the list of BCC recipients as tuples,
            containing the email address and the name of the recipient.
        button_text (str): the text to be used as the button.
        cc (list[tuple(str, str)]): the list of CC recipients as tuples,
            containing the email address and the name of the recipient.
        email (Email): the email to be verified.
        footer_text (str): the text to be used as the footer.
        main_text (str): the text to be used as the body.
        password_update_base_url (str): the base URL (without parameters) to be
            used on the link.
        subject (str): the subject of the email.
        title_text (str): the text to be used as the title.
        user (User): the user resetting the password.
    """

    button_text = None
    password_update_base_url = None
    user = None

    def __init__(self, **kwargs):
        from apps.core.models import User
        self.user = kwargs.get('user', None)

        if not self.user:
            error_msg = _('A value for `user` is required.')
            raise ValueError(error_msg)

        elif not isinstance(self.user, User):
            error_msg = _('`user` must be an instance of `User`.')
            raise ValueError(error_msg)

        super_kwargs = {
            'to': [(self.user.email, self.user.full_name),], }

        hours_to_expire = int(
            settings.PASSWORD_RECOVERY['TOKEN_TIMEOUT'] / 3600)

        defaults = {
            'password_update_base_url': 'https://FRONTEND_URL/PASSWORD_RESET_PATH/',

            'subject': _('Reset your password'),

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

        for attr_name, default_value in defaults.items():
            super_kwargs[attr_name] = kwargs.get(attr_name, default_value)

        super().__init__(**super_kwargs)

    def get_html_body(self):
        """Returns the HTML version of the verification email content.
        """

        password_reset_url = self.get_password_reset_url()
        return (
            f'<h1>{self.title_text}</h1>'
            f'<p>{self.main_text}</p>'
            f'<p><a href="{password_reset_url}">{self.button_text}</a></p>'
            f'<p><em>Direct link: {password_reset_url}</em></p>'
            f'<p>{self.footer_text}</p>'
        )

    def get_password_reset_url(self):
        """Returns the password update URL.
        """

        from django.utils.http import urlencode

        reset_params = {'id': self.user.id,
                        'reset_token': self.user.reset_token}
        return f'{self.password_update_base_url}?{urlencode(reset_params)}'

    def get_plain_text_body(self):
        """Returns the plain text version of the verification email content.
        """

        password_reset_url = self.get_password_reset_url()
        return (
            f'{self.title_text}\n\n'
            f'{self.main_text}\n\n'
            f'Use the following link to reset your password:\n'
            f'{password_reset_url}\n\n'
            f'{self.footer_text}'
        )

    def print(self):
        """Prints the verification email to the console.
        """

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

    def send(self):
        if ('SEND_EMAIL_CALLBACK' not in settings.PASSWORD_RECOVERY
                or not settings.PASSWORD_RECOVERY['SEND_EMAIL_CALLBACK']):
            return super().send()

        callback_name = settings.PASSWORD_RECOVERY['SEND_EMAIL_CALLBACK']
        send_recovery_email = self.get_send_callback(callback_name)
        return send_recovery_email(subject=self.subject,
                                   plain_text=self.get_plain_text_body(),
                                   html=self.get_html_body(),
                                   sender=self.sender,
                                   to=self.to,
                                   cc=self.cc,
                                   bcc=self.bcc,
                                   user_instance=self.user)
