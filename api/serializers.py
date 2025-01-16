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
            'name',
            'date_of_birth',
            'hobbies',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    hobbies = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'date_of_birth', 'hobbies']

    def update(self, instance, validated_data):
        # Handle hobbies by name
        hobbies_data = validated_data.pop('hobbies', [])
        hobbies = []
        for hobby_name in hobbies_data:
            hobby, created = Hobby.objects.get_or_create(name=hobby_name)
            hobbies.append(hobby)
        instance.hobbies.set(hobbies)
        return super().update(instance, validated_data)



class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'accepted', 'created_at']
