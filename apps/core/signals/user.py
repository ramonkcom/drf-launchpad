from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from ..models import (
    Email,
    Person,
)
from ..utils.auth import assign_basic_permissions


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_initial_setup")
def user_initial_setup(sender, instance, created, **kwargs):
    """Initial setup for newly created `User`.

    This function creates a `Person` and an `Email` object for newly created
    `User` objects, and assigns the necessary permissions to it, so it can
    change its own data.

    Args:
        sender (cls): The model triggering the signal (`User`).
        instance (User): The user just saved.
        created (bool): Whether the user was created or not (updated).
    """

    if not created:
        return

    user = instance

    if user.username != settings.ANONYMOUS_USER_NAME:
        Person.objects.create(user=user)

        Email.objects.create(user=user,
                             address=user.email)

        assign_basic_permissions(user)
        assign_perm("view_user", user, user)
        assign_perm("change_user", user, user)
