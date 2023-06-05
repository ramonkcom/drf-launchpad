"""
DATABASES SETTINGS

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

from .common import BASE_DIR

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------- #
