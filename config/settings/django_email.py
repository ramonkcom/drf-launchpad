"""
EMAIL SETTINGS

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

from .common import PROJECT_TITLE

# ---------------------------------------------------------------------------- #
# NOTE: This is a custom setting for the email confirmation functionality.
# TODO: Link documentation for this here.

EMAIL_CONFIRMATION = {
    'CODE_TIMEOUT': 60 * 60 * 24,
    'DEFAULT_FROM': ('noreply@localhost', PROJECT_TITLE),
    'SEND_CALLBACK': '',
}

# ---------------------------------------------------------------------------- #
