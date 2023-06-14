"""
DRF-SPECTACULAR SETTINGS

About drf-spectacular:
- https://drf-spectacular.readthedocs.io/en/latest/

Full list of drf-spectacular settings:
- https://drf-spectacular.readthedocs.io/en/latest/settings.html
"""

from .common import (
    PROJECT_DESCRIPTION,
    PROJECT_TITLE,
    PROJECT_VERSION,
)

SPECTACULAR_SETTINGS = {
    'DESCRIPTION': PROJECT_DESCRIPTION,
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'docExpansion': 'none',
        'tagsSorter': 'alpha',
    },
    'TITLE': PROJECT_TITLE,
    'VERSION': PROJECT_VERSION,
}
