from rest_framework import serializers

from ..models import Email


class EmailSerializer(serializers.ModelSerializer):
    """Serializer for `Email` model.
    """

    class Meta:
        model = Email
        exclude = ['id', 'confirmation_code', 'confirmation_code_date',
                   'origin', 'user',]
        read_only_fields = ['confirmation_date',]
