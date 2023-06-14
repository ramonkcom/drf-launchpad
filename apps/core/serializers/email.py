from rest_framework import serializers

from ..models import Email


class EmailSerializer(serializers.ModelSerializer):
    """Base serializer for `Email`.
    """

    class Meta:
        model = Email
        exclude = ['confirmation_code', 'confirmation_code_date',
                   'origin', 'user',]
        read_only_fields = ['confirmation_date',]
