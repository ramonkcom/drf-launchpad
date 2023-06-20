"""
DRF-GUARDIAN SETTINGS

About Django Guardian:
- https://django-guardian.readthedocs.io/en/stable/

Full list of Django Guardian settings:
- https://django-guardian.readthedocs.io/en/stable/configuration.html#optional-settings
"""

ANONYMOUS_USER_NAME = 'anonymous'
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'utils.permissions.get_anonymous_user'
