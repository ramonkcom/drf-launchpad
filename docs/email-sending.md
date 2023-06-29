🔙 [Back to documentation](./index.md)

---

# Email sending

The default behavior of the system is to send the emails using the Django mail system with a preset text message. However, you can customize both the email sending method with the service of your choice and/or the text of the email message.

When a new user is created or adds a new email address to his/her account, the system creates an instance of [`VerificationEmailMessage`](https://github.com/ramonkcom/drf-launchpad/blob/main/apps/core/mail.py), which is a subclass of [`django.core.mail.EmailMessage`](https://docs.djangoproject.com/en/dev/topics/email/#the-emailmessage-class), and uses it to send the email to the user. The same happens when the user requests a password reset, but in this case an instance of [`PasswordRecoceryEmailMessage`](https://github.com/ramonkcom/drf-launchpad/blob/main/apps/core/mail.py), also a subclass of [`EmailMessage`](https://docs.djangoproject.com/en/dev/topics/email/#the-emailmessage-class), is used.

If you want to customize the email sending method, you can do so by creating your own email sending functions and configuring them in the settings. If you want to customize the text of the email message, you can do so by tweaking the `get_html_body` and `get_plain_text_body` methods of the email sending classes. More on that below.

---

## Configuring Django mail system

If you're fine with the default behavior, you just need to configure the Django mail system in the settings. For instance, if you want to use Gmail, you can do so by adding the following to your `.env` file:

```bash
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=465
EMAIL_HOST_USER="your.email@gmail.com"
EMAIL_HOST_PASSWORD="YOUR_PASSWORD"
DEFAULT_FROM_EMAIL="'Your Name' <your.email@gmail.com>"
```

If you're using PORT 465, make sure that `EMAIL_USE_SSL` is set to `True` in settings:

```python
# config/settings/django_email.py
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False # this have to be False if you're using SSL
```

And if you want to send emails even in development, you should also set the `SEND_EMAIL_IN_DEV` to `True` in settings:

```python
EMAIL_CONFIRMATION = {
    # (...)
    'SEND_EMAIL_IN_DEV': True,
}
```

---

## Customizing the email content

If you want to change the text or the formatting of the email message, you can override the `get_html_body` and `get_plain_text_body` methods on the adequate class.

For instance, if you want to change the text of the email sent to the user when he/she creates a new account, you can do so by overriding the `get_html_body` and `get_plain_text_body` methods of the [`VerificationEmailMessage`](https://github.com/ramonkcom/drf-launchpad/blob/main/apps/core/mail.py) class:

```python

class VerificationEmailMessage:
    def get_body(self):
        return (
            'YOUR CONTENT HERE!\n\n'
            'Customized content.\n\n'
            f'Confirmation code: {self.email_to_verify.confirmation_code}'
        )

    def get_html_body(self):
        return (
            '<h1>YOUR CONTENT HERE!<h1>'
            '<p>Customized content.</p>'
            '<p><strong>Confirmation code:</strong>'
            f'{self.email_to_verify.confirmation_code}</p>'
        )
```

The same applies to the [`PasswordRecoceryEmailMessage`](https://github.com/ramonkcom/drf-launchpad/blob/main/apps/core/mail.py) class.

---

## Customizing the sending method

If you want to use a different email sending method, you can do so by creating your own email sending functions and configuring them in the settings.

First, define your functions (wherever you want):

```python
# apps/core/custom/example.py

def send_confirmation(verification_email_message)
    """Sends the email confirmation message.

    Args:
        verification_email_message (VerificationEmailMessage): The email
            message to be sent.

    Returns:
        int: The number of emails sent.
    """

    # Plug the code to send email confirmation here.
    pass

def send_recovery(password_recovery_email_message)
    """Sends the password recovery email message.

    Args:
        password_recovery_email_message (PasswordRecoceryEmailMessage): The
            email message to be sent.

    Returns:
        int: The number of emails sent.
    """

    # Plug the code to send password recovery email here.
    pass
```

Then, in `config/settings/django_general`:

```python
EMAIL_CONFIRMATION = {
    # (...)
    'SEND_EMAIL_CALLBACK': 'apps.core.custom.example.send_confirmation',
}
```

And in `config/settings/django_auth`:

```python
PASSWORD_RECOVERY = {
    # (...)
    'SEND_EMAIL_CALLBACK': 'apps.core.custom.example.send_recovery',
}
```

Done.

---

🔙 [Back to documentation](./index.md)
