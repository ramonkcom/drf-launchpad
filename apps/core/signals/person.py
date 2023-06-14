from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.db.models.signals import (
    pre_delete,
    pre_save,
)
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from ..models import Person


@receiver(pre_delete, sender=Person, dispatch_uid="prevent_person_direct_deletion")
def prevent_person_direct_deletion(sender, instance, using, origin, **kwargs):
    """Prevents direct `Person` deletion.

    Args:
        sender (cls): The model triggering the signal (`Person`).
        instance (Person): The person being deleted.
        using (str): The database alias being used.
        origin (cls): The Model or QuerySet class originating the deletion.
    """

    if (isinstance(origin, get_user_model()) or (
            isinstance(origin, QuerySet) and origin.model == get_user_model())):
        return

    error_msg = _('Can\'t delete a person directly.')
    raise PermissionDenied(error_msg)


@receiver(pre_save, sender=Person, dispatch_uid="prevent_person_direct_creation")
def prevent_person_direct_creation(sender, instance, **kwargs):
    """Prevents direct `Person` creation.

    Args:
        sender (cls): The model triggering the signal (`Person`).
        instance (Person): The person being saved.
    """

    if getattr(instance, 'user', None):
        return

    error_msg = _('Can\'t create a person directly.')
    raise PermissionDenied(error_msg)
