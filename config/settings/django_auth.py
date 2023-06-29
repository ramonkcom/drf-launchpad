"""
AUTH SETTINGS

About Django settings:
- https://docs.djangoproject.com/en/dev/topics/settings/

Full list of Django settings:
- https://docs.djangoproject.com/en/dev/ref/settings/
"""

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model

AUTH_USER_MODEL = 'core.User'

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# ---------------------------------------------------------------------------- #
# https://github.com/ramonkcom/drf-launchpad/blob/main/docs/custom-settings-and-flags.md#password_recovery

PASSWORD_RECOVERY = {
    'FRONTEND_BASE_URL': 'https://FRONTEND_URL/PASSWORD_RESET_PATH/',
    'SEND_EMAIL_CALLBACK': '',
    'SEND_EMAIL_IN_DEV': False,
    'TOKEN_TIMEOUT': 60 * 60 * 24,
}

# ---------------------------------------------------------------------------- #
