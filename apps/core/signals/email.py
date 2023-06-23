from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from ..models import Email


@receiver(post_save, sender=Email, dispatch_uid="assign_email_permissions")
def assign_email_permissions(sender, instance, created, **kwargs):
    """Adds the basic permissions to handle `Email` objects.

    Adds the necessary permissions to the user so it can view, change and
    delete its own `Email` objects.

    Args:
        sender (cls): The model triggering the signal (`User`).
        instance (User): The user just saved.
        created (bool): Whether the user was created or not (updated).
    """

    if not created:
        return

    email = instance
    user = email.user

    assign_perm("view_email", user, email)
    assign_perm("change_email", user, email)
    assign_perm("delete_email", user, email)
