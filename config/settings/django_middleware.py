"""
APPLICATION SETTINGS

About Django middlewares:
- https://docs.djangoproject.com/en/dev/topics/http/middleware/

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-MIDDLEWARE

MIDDLEWARE = [
    # DJANGO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------------------------- #
