from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("phone", "city", "avatar", "email")
