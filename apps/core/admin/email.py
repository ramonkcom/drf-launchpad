from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _
from django.core import exceptions

from ..models import Email


class EmailInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            data = form.cleaned_data
            email = form.instance

            if (data.get('DELETE') and email.is_primary):
                error_msg = _('You cannot delete the primary email.')
                raise exceptions.ValidationError(error_msg)


class EmailInline(admin.StackedInline):
    extra = 0
    formset = EmailInlineFormSet
    model = Email
    verbose_name = _('email')
    readonly_fields = [
        'confirmation_code', 'confirmation_code_date', 'origin',
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    ('address', 'origin',),
                    ('confirmation_code', 'confirmation_code_date',
                     'confirmation_date',),
                ),
            }),
        )

        return fieldsets
