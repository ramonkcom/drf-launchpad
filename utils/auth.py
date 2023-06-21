from django.utils.translation import gettext_lazy as _


def user_authentication_rule(user):
    """User authentication rule for Simple JWT.

    Args:
        user (User): The user to be authenticated.

    Returns:
        bool: Whether the user can be considered authenticated or not.
    """

    return user is not None and user.is_active
