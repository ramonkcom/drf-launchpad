from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Profile


class ProfileInline(admin.StackedInline):
    can_delete = False
    extra = 0
    model = Profile
    verbose_name = _('profile information')

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    ('given_name', 'family_name',),
                ),
            }),
        )

        return fieldsets
