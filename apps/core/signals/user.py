from datetime import datetime

from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from utils.permissions import assign_basic_permissions

from ..models import (
    Email,
    Person,
)


@receiver(signals.pre_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="generate_username")
def generate_username(sender, instance, **kwargs):
    """Generates a username for the `User` being saved.

    This function generates a username for the `User` being saved, if it
    doesn't have one already. The username is generated from the user's email
    address, and if it already exists, a numeric sequence based on the
    timestamp is appended to it (e.g. `john_12345`).

    Args:
        sender (cls): The model triggering the signal (`User`).
        instance (User): The user being saved.
    """

    user = instance
    if user.username:
        return

    base_username = user.email.split('@')[0]
    generated_username = base_username

    while sender.objects.filter(username=generated_username).exists():
        timestamp_slice = str(int(datetime.now().timestamp()))[-5:]
        generated_username = f'{base_username}_{timestamp_slice}'

    user.username = generated_username


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
