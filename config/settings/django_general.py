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
# NOTE this is a custom setting to determine if we are in production or not

PRODUCTION = False

# ---------------------------------------------------------------------------- #
# NOTE this is a custom setting to determine if we are running tests or not

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# ---------------------------------------------------------------------------- #
