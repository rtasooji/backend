from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # field we want to include in our serializer
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5}}

    def create(self, validated_data):
        """
        Create new user with encrypted password and return
        :param validated_data:
        :return:
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update authorized user info
        :param instance:
        :param validated_data:
        :return:
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user authentication object
    """
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'),
                            username=email,
                            password=password)
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg,
                                              code='authentication_failed')
        attrs['user'] = user
        return attrs
