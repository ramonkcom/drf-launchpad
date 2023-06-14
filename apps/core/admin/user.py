from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from ..models import User
from .person import PersonInline


class UserAdmin(auth_admin.UserAdmin):
    """Defines the admin interface for the `User` model.
    """

    class Media:
        css = {
            'all': ('css/custom.css', 'core/css/admin.css',)
        }

    inlines = [PersonInline,]

    readonly_fields = ['date_joined',]

    list_display = ['id', 'email', 'username', 'full_name', 'date_joined',
                    'is_active', 'is_staff', 'is_superuser',]

    list_display_links = ['id', 'email', 'username',]

    list_filter = ['is_active', 'is_staff', 'is_superuser',]

    search_fields = ['username', 'email', 'emails__address',
                     'person__given_name', 'person__family_name',]

    def get_fieldsets(self, request, obj=None):
        """Returns the fieldsets for the `User` change pages.
        """

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


admin.site.register(User, UserAdmin)
