"""
GENERAL SETTINGS

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-SECRET_KEY

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-DEBUG

DEBUG = True

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts

ALLOWED_HOSTS = []

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf

ROOT_URLCONF = 'config.urls'

# ---------------------------------------------------------------------------- #
# NOTE: This is a custom setting to determine if we are in production or not.
# TODO: Link documentation for this here.

PRODUCTION = False

# ---------------------------------------------------------------------------- #
# NOTE: This is a custom setting to determine if we are running tests or not.
# TODO: Link documentation for this here.

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# ---------------------------------------------------------------------------- #
# NOTE: This is a custom setting for the email confirmation functionality.
# TODO: Link documentation for this here.

EMAIL_CONFIRMATION = {
    'CODE_TIMEOUT': 60 * 60 * 24,
}

# ---------------------------------------------------------------------------- #
