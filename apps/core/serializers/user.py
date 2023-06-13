from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .email import EmailSerializer
from .person import PersonSerializer
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for `User` model.
    """

    class Meta:
        model = User
        exclude = [
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'password',
            'user_permissions',
        ]

    def get_fields(self):
        fields = super().get_fields()

        person_serializer = PersonSerializer()
        for field_name, field in person_serializer.get_fields().items():
            field.source = f'person.{field_name}'
            fields[field_name] = field

        fields['password_1'] = serializers.CharField(write_only=True)
        fields['password_2'] = serializers.CharField(write_only=True)
        fields['emails'] = EmailSerializer(many=True, read_only=True)

        return fields

    def validate(self, data):  # pylint: disable=arguments-renamed
        data.pop('password', None)

        password_1 = data.pop('password_1', None)
        password_2 = data.pop('password_2', None)

        if not password_1 and not password_2:
            return data

        if password_1 != password_2:
            error_msg = _('Passwords must match.')
            raise serializers.ValidationError(
                {'password_2': error_msg})

        data['password'] = password_1
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('email', None)

        person = validated_data.pop('person', {})
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        if person:
            serializer = PersonSerializer(
                user.person, data=person, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return user