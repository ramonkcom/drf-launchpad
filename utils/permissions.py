from django.conf import settings


def assign_basic_permissions(user):
    """Assigns the basic permissions to an user.

    This function assigns the basic permissions to an user (usually a newly
    created one), so it can handle its own data.

    Args:
        user (User): The user to be assigned the permissions.

    Returns:
        User: The user with the assigned permissions.
    """

    from guardian.shortcuts import assign_perm

    assign_perm('core.view_user', user)
    assign_perm('core.change_user', user)

    assign_perm('core.view_email', user)
    assign_perm('core.add_email', user)
    assign_perm('core.change_email', user)
    assign_perm('core.delete_email', user)

    return user


def get_anonymous_user(user_model):
    """Creates an anonymous user. This is necessary for 'django-guardian'.

    See: https://django-guardian.readthedocs.io/en/stable/userguide/custom-user-model.html#custom-user-model-anonymous

    Args:
        user_model (cls): The system user model.

    Returns:
        User: The created anonymous user.
    """

    return user_model(username=settings.ANONYMOUS_USER_NAME)
