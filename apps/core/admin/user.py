from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .email import EmailInline
from ..models import User
from .profile import ProfileInline


class UserAdmin(auth_admin.UserAdmin):

    class Media:
        css = {
            'all': ('css/custom.css', 'core/css/admin.css',)
        }

    inlines = [ProfileInline, EmailInline,]

    readonly_fields = ['date_joined',]

    list_display = ['id', 'email', 'username', 'full_name', 'date_joined',
                    'is_active', 'is_staff', 'is_superuser',]

    list_display_links = ['id', 'email', 'username',]

    list_filter = ['is_active', 'is_staff', 'is_superuser',]

    search_fields = ['username', 'email', 'emails__address',
                     'profile__given_name', 'profile__family_name',]

    def get_fieldsets(self, request, obj=None):

        fieldsets = (
            (_('Credentials'), {
                'fields': (
                    'date_joined',
                    ('email', 'username',),
                    'password',
                ),
            }),
            (_('Roles'), {
                'fields': (
                    ('is_active', 'is_staff', 'is_superuser',),
                ),
            }),
            (_('Permissions'), {
                'fields': (
                    'groups',
                    'user_permissions',
                ),
            }),
        )

        if not obj:
            fieldsets[0][1]['fields'] = (
                ('email', 'username',),
                'password1',
                'password2',
            )

        return fieldsets

    def save_related(self, request, form, formsets, change):
        from ..models import Email

        for formset in formsets:
            for inline_form in formset.forms:
                if not isinstance(inline_form.instance, Email):
                    continue

                if Email.objects.filter(id=inline_form.instance.pk).exists():
                    continue

                new_email = inline_form.instance
                new_email.origin = Email.Origin.ADMIN

        super().save_related(request, form, formsets, change)


admin.site.register(User, UserAdmin)
