🔙 [Back to documentation](./index.md)

---

# Custom settings and flags

There are two custom settings in DRF Launchpad: [`EMAIL_CONFIRMATION`](#email_confirmation), which is used to configure the email confirmation process, and [`PASSWORD_RESET`](#password_reset), which is used to configure the password recovery process.

There is also two flags: [`TESTING`](#testing), which is automatically set to `True` when running tests, and [`PRODUCTION`](#production), which you can set to `True` to know when you're running in production.

---

## `EMAIL_CONFIRMATION`

The `EMAIL_CONFIRMATION` setting is located in the `config/settings/django_general.py` file. It is used to configure the email confirmation process.

```python
EMAIL_CONFIRMATION = {
    # The frontend base URL to confirm the email
    'FRONTEND_BASE_URL': 'https://FRONTEND_URL/CONFIRM_EMAIL_PATH/',

    # The time period in second the user can use the code to confirm the email
    'CODE_TIMEOUT': 60 * 60 * 24,

    # The callback to send the email confirmation
    'SEND_EMAIL_CALLBACK': '',

    # Whether to send the email even in development
    'SEND_EMAIL_IN_DEV': False,
}
```

You can read more about the `SEND_EMAIL_CALLBACK` setting in the [email sending section](./email-sending.md#using-callbacks).

---

## `PASSWORD_RESET`

The `PASSWORD_RESET` setting is located in the `config/settings/django_auth.py` file. It is used to configure the password recovery process.

```python
PASSWORD_RESET = {
    # The frontend base URL to reset the password
    'FRONTEND_BASE_URL': 'https://FRONTEND_URL/PASSWORD_RESET_PATH/',

    # The callback to send the password recovery email
    'SEND_EMAIL_CALLBACK': '',

    # Whether to send the recovery email even in development
    'SEND_EMAIL_IN_DEV': False,

    # The time period in second the user can use the token to recover the password
    'TOKEN_TIMEOUT': 60 * 60 * 24,
}
```

You can read more about the `SEND_EMAIL_CALLBACK` setting in the [email sending section](./email-sending.md#using-callbacks).

---

## `TESTING`

This not a setting, but a flag that is automatically set to `True` when running tests. It is used, for instance, to avoid sending emails during tests. You don't need to worry about it. You just need to know that it is available for you to use:

```python
from django.conf import settings

if settings.TESTING:
    # You're in tests! Do something.

else:
    # You're not in tests! Do something else.
```

---

## `PRODUCTION`

This not a setting, but a flag that you can set to `True` to know when you're running in production:

```python
from django.conf import settings

if settings.PRODUCTION:
    # You're in production! Do something.

else:
    # You're not in production! Do something else.
```

---

🔙 [Back to documentation](./index.md)
