from rest_framework import serializers

from ..models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Serializer for `Person` model.
    """

    class Meta:
        model = Person
        exclude = ['id', 'user',]
