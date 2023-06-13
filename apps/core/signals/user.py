from guardian.shortcuts import assign_perm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from ..models import (
    Email,
    Person,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_initial_setup")
def user_initial_setup(sender, instance, created, **kwargs):
    """Initial setup for newly created `User`.

    This function creates a `Person` and an `Email` objects for newly created
    `User` objects, and assigns the necessary permissions to it, so it can
    change its own data.

    Args:
        sender (cls): The model triggering the signal (`User`).
        instance (User): The user just saved.
        created (bool): Whether the user was created or not (updated).
    """

    if not created:
        return

    if instance.username != settings.ANONYMOUS_USER_NAME:
        Person.objects.create(user=instance)
        Email.objects.create(user=instance,
                             address=instance.email)
        assign_perm("core.change_user", instance)
        assign_perm("change_user", instance, instance)
