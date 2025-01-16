"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# api/urls.py

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
    current_user_view,  # Added this import
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
    path('api/users/current/', current_user_view, name='current-user'),  # Added this route
    path('api/friend-requests/', friend_request_view, name='friend-request'),
    path('api/hobbies/', hobby_list_create_view, name='hobbies-view'),
]



