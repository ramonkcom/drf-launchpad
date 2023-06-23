from uuid import uuid4

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Represents the profile data of an user in the system.

    Attributes:
        id (uuid): The unique identifier of the user.
        given_name (str): The given name of the user.
        family_name (str): The family name of the user.
    """

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        ordering = ['family_name', 'given_name',]

    # ---------------------------------- FIELDS ---------------------------------- #

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        to='core.User',
        on_delete=models.CASCADE,
        related_name='profile',
        related_query_name='profile',
        verbose_name=_('user'),
    )

    given_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validators.MinLengthValidator(3),],
        verbose_name=_('given name'),
    )

    family_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validators.MinLengthValidator(3),],
        verbose_name=_('family name'),
    )

    # -------------------------------- PROPERTIES -------------------------------- #

    @classmethod
    @property
    def factory(self):
        """Returns the factory for the `Profile` model.

        Returns:
            ProfileFactory: The factory for the `Profile` model.
        """

        from ..factories import ProfileFactory
        return ProfileFactory

    @property
    def full_name(self) -> str:
        """Returns the full name of the profile.

        Returns the given name followed by the family name of the profile.

        Returns:
            str: The full name of the profile.
        """

        full_name = ' '.join(
            [n for n in [self.given_name, self.family_name,] if n])

        return full_name

    # ---------------------------------- METHODS --------------------------------- #

    def __str__(self) -> str:
        representation = self.full_name

        if not representation:
            representation = str(self.user)

        return representation
