from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.fields import CharField
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from cartool.utils.token_generator import OTPVerifyTokenGenerator
from user.models import User


class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = PasswordField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = {}
        try:
            user = User.objects.get(phone_number=attrs['phone_number'])
            if user.check_password(attrs['password']):
                refresh = self.get_token(user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                if api_settings.UPDATE_LAST_LOGIN:
                    update_last_login(None, user)
            else:
                raise AuthenticationFailed({'password': [_('პაროლი არასწორია')]})
        except User.DoesNotExist:
            raise AuthenticationFailed({'phone_number': [_('მოცემული ნომრით არ მოიძებნა მომხმარებელი')]})

        return data


class UserCreateSerializer(serializers.ModelSerializer):
    password = CharField(write_only=True, validators=[validate_password])
    password2 = CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'phone_number',
            'password', 'password2',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'password': {'required': True},
            'password2': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': _('პაროლის ფილდები ერთმანეთს არ დაემთხვა'),
                'password2': _('პაროლის ფილდები ერთმანეთს არ დაემთხვა'),
            })

        return attrs

    def create(self, validated_data) -> 'User':
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)