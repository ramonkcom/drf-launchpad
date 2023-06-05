"""
SIMPLE JWT SETTINGS

About Django REST Framework:
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Full list of Django REST Framework settings:
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
"""

from datetime import timedelta


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ['Bearer', 'JWT',],
}
