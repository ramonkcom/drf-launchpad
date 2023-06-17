from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from ..models import (
    Email,
    Person,
)
from ..utils.permissions import assign_basic_permissions


@receiver(signals.post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_initial_setup")
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

    user = instance
    if user.is_anonymous:
        return

    person_kwargs = getattr(user, '_person_attrs', {})

    if created:
        Email.objects.create(user=user,
                             address=user.email)

        if not getattr(sender, '_skip_person_creation', False):
            person_kwargs['user'] = user
            Person.objects.create(**person_kwargs)

        assign_basic_permissions(user)
        assign_perm("view_user", user, user)
        assign_perm("change_user", user, user)

    else:
        if person_kwargs:
            for field_name, value in person_kwargs.items():
                setattr(user.person, field_name, value)

        user.person.save()
