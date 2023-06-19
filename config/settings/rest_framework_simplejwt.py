"""
SIMPLE JWT SETTINGS

About Simple JWT:
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Full list of Simple JWT settings:
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
"""

from datetime import timedelta


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'AUTH_HEADER_TYPES': ['JWT',],
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_AUTHENTICATION_RULE': 'apps.core.utils.auth.user_authentication_rule',
}
