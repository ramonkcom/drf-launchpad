"""
DJANGO REST FRAMEWORK SETTINGS

About Django REST Framework:
- https://www.django-rest-framework.org/

Full list of Django REST Framework settings:
- https://www.django-rest-framework.org/api-guide/settings/
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.DjangoObjectPermissions',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 12,
}
