from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


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