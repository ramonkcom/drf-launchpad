"""
STATIC FILES SETTINGS

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

from .common import BASE_DIR

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-STATIC_URL

STATIC_URL = 'static/'

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-STATICFILES_DIRS

STATICFILES_DIRS = [
    BASE_DIR / os.path.join('config', 'static'),
]

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-STATIC_ROOT

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------------------------------------------------- #
