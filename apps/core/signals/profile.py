from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import (
    QuerySet,
    signals,
)
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from ..models import Profile


@receiver(signals.pre_delete, sender=Profile, dispatch_uid="prevent_profile_direct_deletion")
def prevent_profile_direct_deletion(sender, instance, using, origin, **kwargs):
    """Prevents direct deletion of a profile.

    Args:
        sender (cls): The model triggering the signal (`Profile`).
        instance (Profile): The profile being deleted.
        using (str): The database alias being used.
        origin (cls): The Model or QuerySet class originating the deletion.
    """

    if (isinstance(origin, get_user_model()) or (
            isinstance(origin, QuerySet) and origin.model == get_user_model())):
        return

    error_msg = _('Can\'t delete a profile directly.')
    raise PermissionDenied(error_msg)
