🔙 [Back to documentation](./index.md)

---

# Email sending

In order for everything to work as designed, you need to set up an email sending service for sending email confirmation and password recovery emails.

The way things currently work is that when the user is created or adds a new email address to his/her account, the system uses a `VerificationEmailMessage` instance to mount the email message and send it to the user. The same happens when the user requests a password reset, but in this case a `PasswordResetEmailMessage` instance will be used.

Both classes live in `utils/mail.py` and share a lot of similarities, as they inherit from the same base class (`EmailMessage`). The main differences between them are in the `get_html_body` and `get_plain_text_body` methods, which are responsible for generating the HTML and plain text versions of the email message.

There are a few ways you can plug your email sending service into this classes. The most straightforward way is to customize the `get_html_body`, `get_plain_text_body` and `send` methods in these classes. But you can also avoid touching these classes by creating your own callbacks and configuring them in the settings.

We'll go through both approaches in the following sections.

---

## Customizing the email sending classes

If you opt to customize the email sending classes, the only required step is to implement your own version of the `send` method with your email sending service of choice. The default implementation does not try to send emails:

```python

class EmailMessage:

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

```

If you want to change the text or the formatting of the email message, you can override the `get_html_body` and `get_plain_text_body` methods on the adequate class.

But if just want to change the text, you can do so directly in the views (`UserCreateAPIView`, `EmailConfirmationAPIView`, `PasswordRecoveryAPIView`). For instance:

```python
class PasswordRecoveryAPIView(views.APIView):
    # (...)

    def post(self, request, *args, **kwargs):
        # (...)

        reset_email = user.get_password_reset_email(
            subject='CUSTOM SUBJECT',
            title_text='CUSTOM TITLE',
            main_text='CUSTOM MAIN TEXT',
            button_text='CUSTOM BUTTON',
            footer_text='CUSTOM FOOTER'
        )
        reset_email.send()

        return response.Response(status=status.HTTP_202_ACCEPTED)

```

---

## Using callbacks

To use callbacks, you need to create a function that will be called by the email sending classes and configure it in the settings. This function should be able to receive the defaults of the email message as arguments.

For instance:

```python
# utils/my_custom_email_callbacks.py

def send_confirmation(subject, # str
                      plain_text, # str
                      html, # str
                      sender, # tuple(str, str)
                      to, # list(tuple(str, str))
                      cc, # list(tuple(str, str))
                      bcc, # list(tuple(str, str))
                      email_instance) # core.Email
    # Plug the code to send email confirmation here.
    pass

def send_recovery(subject, # str
                  plain_text, # str
                  html, # str
                  sender, # tuple(str, str)
                  to, # list(tuple(str, str))
                  cc, # list(tuple(str, str))
                  bcc, # list(tuple(str, str))
                  user_instance) # core.User
    # Plug the code to send password recovery email here.
    pass
```

Then, in `config/settings/django_general`:

```python
EMAIL_CONFIRMATION = {
    # (...)
    'SEND_CALLBACK': 'utils.my_custom_email_callbacks.send_confirmation',
}
```

And in `config/settings/django_auth`:

```python
PASSWORD_RECOVERY = {
    # (...)
    'SEND_CALLBACK': 'utils.my_custom_email_callbacks.send_recovery',
}
```

Done.

---

🔙 [Back to documentation](./index.md)
