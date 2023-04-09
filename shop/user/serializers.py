from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import User


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    email = serializers.EmailField(
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            attrs['user'] = user
            return attrs


class RegistrSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    username = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ["email", "fullname", "password", "password2", "username"]

    def save(self, **kwargs):
        user = User()
        user.email = self.validated_data["email"]
        user.fullname = self.validated_data["fullname"]
        if self.validated_data["password"] and self.validated_data["password"] == self.validated_data["password2"]:
            user.set_password(self.validated_data["password"])
            user.save()
            return user
        return serializers.ValidationError({"password": "Password not valid"})
