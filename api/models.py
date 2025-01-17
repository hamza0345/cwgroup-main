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
    name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # Each user can have multiple hobbies, and each hobby can belong to multiple users
    hobbies = models.ManyToManyField(Hobby, blank=True, related_name='users_with_this_hobby')

    def friends(self):
        """
        Return a queryset of users who are friends (i.e. accepted FriendRequest)
        with this user.
        We consider both directions: if I'm from_user or to_user.
        """
        from .models import FriendRequest

        # Friend requests that this user sent AND were accepted
        sent = FriendRequest.objects.filter(
            from_user=self, accepted=True
        ).values_list('to_user', flat=True)

        # Friend requests that this user received AND were accepted
        received = FriendRequest.objects.filter(
            to_user=self, accepted=True
        ).values_list('from_user', flat=True)

        # Combine these user IDs
        friend_ids = list(sent) + list(received)
        return CustomUser.objects.filter(id__in=friend_ids)


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
