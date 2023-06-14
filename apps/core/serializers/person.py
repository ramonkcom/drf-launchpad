from rest_framework import serializers

from ..models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Base serializer for `Person`.
    """

    class Meta:
        model = Person
        exclude = ['id', 'user',]
