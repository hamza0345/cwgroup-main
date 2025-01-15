# api/serializers.py

from rest_framework import serializers
from .models import CustomUser, Hobby, FriendRequest


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    """
    Serialises our CustomUser, including date_of_birth and hobbies.
    """
    hobbies = HobbySerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'date_of_birth',
            'hobbies',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    A separate serializer if you want to allow editing certain fields
    (name, email, date_of_birth, hobbies, etc.)
    """
    # By default, fields that are M2M must be handled carefully.
    # We'll treat hobbies as a list of hobby names or IDs, see update logic in the view.
    hobbies = serializers.PrimaryKeyRelatedField(queryset=Hobby.objects.all(), many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'date_of_birth', 'hobbies']


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'accepted', 'created_at']
