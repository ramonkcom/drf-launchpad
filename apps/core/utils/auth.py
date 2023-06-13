from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from django.conf import settings


def user_authentication_rule(user):
    """User authentication rule for Simple JWT.

    Args:
        user (User): The user to be authenticated.

    Returns:
        bool: Whether the user can be considered authenticated or not.

    Raises:
        AuthenticationFailed: If the user email is not confirmed.
    """

    if not user.is_email_confirmed:
        error_msg = _('Email is not confirmed.')
        raise exceptions.AuthenticationFailed({'email': error_msg})

    return user is not None and user.is_active


def get_anonymous_user(user_model):
    """Creates an anonymous user. This is necessary for 'django-guardian'.

    See: https://django-guardian.readthedocs.io/en/stable/userguide/custom-user-model.html#custom-user-model-anonymous

    Args:
        user_model (cls): The `User` model.

    Returns:
        User: The created anonymous user.
    """

    return user_model(username=settings.ANONYMOUS_USER_NAME)
