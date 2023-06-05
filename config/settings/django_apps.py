"""
APPLICATION SETTINGS

About Django applications:
- https://docs.djangoproject.com/en/dev/ref/applications/

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-INSTALLED_APPS

INSTALLED_APPS = [
    # DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD-PARTY
    'drf_spectacular',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # PROJECT
    'apps.core.apps.CoreConfig',
]

# ---------------------------------------------------------------------------- #
