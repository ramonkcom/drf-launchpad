import factory

from utils.factories.mixins import DictFactoryMixin

from ..models import Profile


class ProfileFactory(DictFactoryMixin,
                     factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    family_name = factory.Faker('last_name')

    given_name = factory.Faker('first_name')
