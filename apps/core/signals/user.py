from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from ..models import Person


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_person_for_user")
def create_person_for_user(sender, instance, created, **kwargs):
    """Creates a `Person` for newly created `User`.

    This function creates a `Person` object everytime an User object is
    created, and then relates both of them.

    Args:
        sender (cls): The model triggering the signal (`User`).
        instance (User): The user just saved.
        created (bool): Whether the user was created or not (updated).
    """

    if not created:
        return

    Person.objects.create(user=instance)
