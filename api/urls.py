"""project URL Configuration
"""
from django.urls import path
from .views import (
    main_spa,
    signup_view,
    login_view,
    logout_view,
)
from .views_api import (
    user_list_view,
    user_detail_view,
    friend_request_view,
    hobby_list_create_view,
    current_user_view,
    current_user_friends_view,
)

urlpatterns = [
    # SSR routes
    path('', main_spa, name='main-spa'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # RESTful endpoints
    path('api/users/', user_list_view, name='user-list'),
    path('api/users/<int:user_id>/', user_detail_view, name='user-detail'),
    path('api/users/current/', current_user_view, name='current-user'),
    path('api/friend-requests/', friend_request_view, name='friend-request'),
    path('api/hobbies/', hobby_list_create_view, name='hobbies-view'),
    path('api/users/current/friends/', current_user_friends_view, name='current-user-friends'),

]
