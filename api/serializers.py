# api/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, Hobby, FriendRequest

User = get_user_model()

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    """
    Serialises our CustomUser, including date_of_birth and hobbies,
    plus how many hobbies in common with the requesting user (if annotated).
    """
    hobbies = HobbySerializer(many=True, read_only=True)
    # We'll allow an integer field for common hobbies
    common_hobbies = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'name',
            'date_of_birth',
            'hobbies',
            'common_hobbies',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Handles updating user data, including hobbies by name,
    plus optional username/password changes.
    """
    hobbies = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'name',
            'email', 'date_of_birth', 'hobbies'
        ]

    def validate_username(self, value):
        """Ensure the username is unique if changed."""
        if CustomUser.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def update(self, instance: CustomUser, validated_data: dict) -> CustomUser:
        # Handle hobbies by name
        hobbies_data = validated_data.pop('hobbies', [])
        if hobbies_data:
            hobbies = []
            for hobby_name in hobbies_data:
                hobby, created = Hobby.objects.get_or_create(name=hobby_name)
                hobbies.append(hobby)
            instance.hobbies.set(hobbies)

        # Update the password if provided
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        # Update the username if provided
        username = validated_data.pop('username', None)
        if username:
            instance.username = username

        return super().update(instance, validated_data)


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    to_user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'accepted', 'created_at']
