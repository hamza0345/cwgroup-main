from django.db import models
from django.contrib.auth.models import AbstractUser
from typing import List

class Hobby(models.Model):
    """
    Represents a hobby that any user can add to their profile.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class CustomUser(AbstractUser):
    """
    Our custom User model. Must match the 'api.CustomUser' reference in settings.py.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True, related_name='users_with_this_hobby')

    @property
    def name(self) -> str:
        return self.first_name or ""

class FriendRequest(models.Model):
    """
    A friend request from one user to another.
    """
    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friend_requests_sent'
    )
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friend_requests_received'
    )
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self) -> str:
        status = "Accepted" if self.accepted else "Pending"
        return f"FriendRequest from {self.from_user.username} to {self.to_user.username} ({status})"

class PageView(models.Model):
    """
    Example model from your snippet, representing page view count.
    """
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
