"""
EMAIL SETTINGS

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

from dotenv import load_dotenv

from .common import PROJECT_TITLE

load_dotenv()

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port

EMAIL_PORT = os.getenv('EMAIL_PORT', 587)

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls

EMAIL_USE_TLS = False

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-ssl

EMAIL_USE_SSL = True

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@localhost')

# ---------------------------------------------------------------------------- #
# https://github.com/ramonkcom/drf-launchpad/blob/main/docs/custom-settings-and-flags.md#email_confirmation

EMAIL_CONFIRMATION = {
    'FRONTEND_BASE_URL': 'https://FRONTEND_URL/CONFIRM_EMAIL_PATH/',
    'CODE_TIMEOUT': 60 * 60 * 24,
    'SEND_EMAIL_CALLBACK': '',
    'SEND_EMAIL_IN_DEV': False,
}

# ---------------------------------------------------------------------------- #
