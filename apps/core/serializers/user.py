from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .email import EmailSerializer
from ..models import User
from .profile import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'password',
            'reset_token',
            'reset_token_date',
            'user_permissions',
        ]
        read_only_fields = [
            'date_joined',
        ]

    def get_fields(self):
        fields = super().get_fields()

        profile_serializer = ProfileSerializer()
        for field_name, field in profile_serializer.get_fields().items():
            field.source = f'profile.{field_name}'
            fields[field_name] = field

        fields['password_1'] = serializers.CharField(write_only=True)
        fields['password_2'] = serializers.CharField(write_only=True)
        fields['emails'] = EmailSerializer(many=True, read_only=True)

        return fields

    def validate(self, data):  # pylint: disable=arguments-renamed
        data.pop('password', None)
        password_1 = data.pop('password_1', None)
        password_2 = data.pop('password_2', None)

        if password_1 != password_2:
            error_msg = _('Passwords must match.')
            raise serializers.ValidationError(
                {'password_2': error_msg})

        if password_1:
            data['password'] = password_1

        profile = data.pop('profile', {})
        for field_name, value in profile.items():
            data[field_name] = value

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
