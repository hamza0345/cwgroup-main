from django.contrib import admin
from .models import CustomUser, Hobby, FriendRequest, PageView

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth')

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'accepted', 'created_at')

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'count')
