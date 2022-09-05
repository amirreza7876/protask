from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data['username'], password=validated_data['password'],
                                              email=validated_data['email'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username']
        # id
        # password
        # last_login
        # phone_number
        # email
        # username
        # firstname
        # lastname
        # is_active
        # is_superuser
        # is_staff
        # groups
        # user_permissions

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         return token


# class MyTokenVerifySerializer(TokenVerifySerializer):
#     def validate(self, attrs):
#         token = attrs['token']
#         print(type(token))
#         user = Token.objects.get(key=token)
#         # print(user)
#         super().validate(attrs)
#         return {'code': 'token is valid'}
