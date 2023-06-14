from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Person


class PersonInline(admin.StackedInline):
    can_delete = False
    extra = 0
    model = Person
    verbose_name = _('personal information')

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    ('given_name', 'family_name',),
                ),
            }),
        )

        return fieldsets
