import factory

from apps.mixins import DictFactoryMixin

from ..models import Email


class EmailFactory(DictFactoryMixin,
                   factory.django.DjangoModelFactory):

    class Meta:
        model = Email

    address = factory.Faker('ascii_safe_email')
