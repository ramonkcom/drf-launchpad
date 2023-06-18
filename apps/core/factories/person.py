import factory
import uuid

from apps.mixins import DictFactoryMixin

from ..models import Person


class PersonFactory(DictFactoryMixin,
                    factory.django.DjangoModelFactory):

    class Meta:
        model = Person

    family_name = factory.Faker('last_name')

    given_name = factory.Faker('first_name')
