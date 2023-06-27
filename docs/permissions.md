🔙 [Back to documentation](./index.md)

---

# Permissions

DRF Lauchpad uses the Django native implementation of `DjangoModelPermissions` for model level permissions and the [Guardian](https://django-guardian.readthedocs.io/en/stable/)'s implementation of `DjangoObjectPermissions` for object level permissions. These permissions are the default ones for all the views in the project, and this is defined in the `DEFAULT_PERMISSION_CLASSES` setting in the `config/settings/rest_framework.py` file:

```python
REST_FRAMEWORK = {
    # (...)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.DjangoObjectPermissions',
    ],
    # (...)
}
```

In the current implementation, permissions are assigned to `User` in two moments. First, upon `User` creation, the `User` is assigned the basic permissions to handle its own data. This assignment happens in the in the `assign_initial_permissions` function (`utils/permissions.py`), which is called by the `User`'s `post_save` signal.

This function is decoupled from the signals file for convenience, as you might want to add new permissions to the `User` upon its creation as you add new models to your project.

The second moment permissions are assigned to `User` happens upon `Email` creation, when the `User` is assigned the necessary permissions to handle its emails. The assignment happens in the `assign_email_permissions` function, defined in the signals file for `Email` (`apps/core/signals/email.py`). You won't need to change this function most of the times.

---

🔙 [Back to documentation](./index.md)
