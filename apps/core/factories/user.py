from datetime import datetime

from django.contrib.auth import get_user_model
import factory
from faker import Faker

from apps.mixins import DictFactoryMixin


User = get_user_model()
fake = Faker()


def build_username(obj):
    base_username = f'{obj.given_name}_{obj.family_name}'.lower()
    username = base_username

    while User.objects.filter(username=username).exists():
        timestamp_slice = str(int(datetime.now().timestamp()))[-5:]
        username = f'{base_username}_{timestamp_slice}'

    return username


class UserFactory(DictFactoryMixin,
                  factory.django.DjangoModelFactory):

    class Meta:
        model = User

    class Params:
        given_name = factory.Faker('first_name')
        family_name = factory.Faker('last_name')

    email = factory.LazyAttribute(
        lambda o: f'{o.username}@{fake.domain_name()}')

    is_staff = False

    is_superuser = False

    password = factory.Faker('password')

    person = factory.RelatedFactory(
        'apps.core.factories.PersonFactory',
        factory_related_name='user',
        given_name=factory.SelfAttribute('..given_name'),
        family_name=factory.SelfAttribute('..family_name'),
    )

    username = factory.LazyAttribute(build_username)

    @classmethod
    def _generate(cls, strategy, params):
        setattr(User, '_skip_person_creation', True)
        return_value = super()._generate(strategy, params)
        setattr(User, '_skip_person_creation', False)
        return return_value

    @classmethod
    def build_dict(cls, **kwargs):
        include_fields = kwargs.pop('include_fields', [])
        exclude_fields = kwargs.pop('exclude_fields', [])

        user = cls.build()

        user_dict = cls._build_dict(user, **kwargs)
        person_dict = cls._build_dict(user.person, **kwargs)
        user_dict.update(person_dict)

        exclude_fields.extend(f for f in [
            'id',
            'date_joined',
            'groups',
            'last_login',
            'user',
            'user_permissions',
        ] if f not in include_fields)

        return cls._filter_fields(user_dict,
                                  include_fields,
                                  exclude_fields)
