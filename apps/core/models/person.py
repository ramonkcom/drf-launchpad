from uuid import uuid4

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core import validators


class Person(models.Model):
    """Represents an user in the system.

    Attributes:
        id (uuid): The unique identifier of the user.
        given_name (str): The given name of the user.
        family_name (str): The family name of the user.
    """

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
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
        related_name='person',
        related_query_name='person',
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

    # ---------------------------------- METHODS --------------------------------- #

    def __str__(self) -> str:
        """Returns the string representation of the person.

        Returns the given name followed by the family name of the person. If any
        of them is not set, returns the email.

        Returns:
            str: The string representation of the person.
        """

        representation = ' '.join(
            [n for n in [self.given_name, self.family_name,] if n])

        if not representation:
            representation = str(self.user)

        return representation