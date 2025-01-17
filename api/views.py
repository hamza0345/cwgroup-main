# api/views.py (unchanged for SSR)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.conf import settings
from datetime import date, timedelta

from .forms import SignupForm, SigninForm, ProfileUpdateForm
from .models import CustomUser, Hobby, FriendRequest

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    HobbySerializer,
    FriendRequestSerializer
)

def signup_view(request):
    # unchanged SSR approach
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            print(form.errors)
        return render(request, 'api/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'api/signup.html', {'form': form})


def login_view(request):
    # unchanged SSR approach
    if request.method == 'POST':
        form = SigninForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('/')
        return render(request, 'api/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = SigninForm()
    return render(request, 'api/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def main_spa(request):
    # Always load the built spa/index.html
    return render(request, 'api/spa/index.html', {})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Returns the currently authenticated user's details.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_friends_view(request):
    friends_qs = request.user.friends()
    serializer = UserSerializer(friends_qs, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def hobby_list_create_view(request):
    if request.method == 'GET':
        hobbies = Hobby.objects.all()
        serializer = HobbySerializer(hobbies, many=True)
        return Response({'hobbies': serializer.data})

    elif request.method == 'POST':
        hobby_name = request.data.get('hobby_name')
        if not hobby_name:
            return Response({'error': 'No hobby name provided'}, status=status.HTTP_400_BAD_REQUEST)
        hobby_obj, created = Hobby.objects.get_or_create(name=hobby_name)
        response_data = HobbySerializer(hobby_obj).data
        if created:
            return Response({'message': 'Hobby created', 'hobby': response_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Hobby already exists', 'hobby': response_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    today = date.today()
    min_age_str = request.GET.get('min_age')
    max_age_str = request.GET.get('max_age')
    page_str = request.GET.get('page', 1)

    users_qs = CustomUser.objects.exclude(pk=request.user.pk)

    if min_age_str:
        try:
            min_age = int(min_age_str)
            min_birth_date = today - timedelta(days=min_age * 365)
            users_qs = users_qs.filter(date_of_birth__lte=min_birth_date)
        except ValueError:
            pass

    if max_age_str:
        try:
            max_age = int(max_age_str)
            max_birth_date = today - timedelta(days=max_age * 365)
            users_qs = users_qs.filter(date_of_birth__gte=max_birth_date)
        except ValueError:
            pass

    user_hobbies = request.user.hobbies.all()
    users_qs = users_qs.annotate(
        common_hobbies_count=Count(
            'hobbies',
            filter=Q(hobbies__in=user_hobbies),
            distinct=True
        )
    ).order_by('-common_hobbies_count')

    from django.core.paginator import Paginator
    paginator = Paginator(users_qs, 10)
    page_obj = paginator.get_page(page_str)

    serializer = UserSerializer(page_obj, many=True)

    return Response({
        'users': serializer.data,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
    })

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_detail_view(request, user_id: int):
    user_obj = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'PUT' and request.user.id != user_obj.id:
        return Response({'error': 'You cannot edit another user’s profile.'},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def friend_request_view(request):
    if request.method == 'POST':
        to_user_id = request.data.get('to_user_id')
        from_user = request.user

        if from_user.pk == to_user_id:
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        to_user = get_object_or_404(CustomUser, pk=to_user_id)
        fr, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({'error': 'Friend request already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')

        fr_obj = get_object_or_404(FriendRequest, pk=friend_request_id)
        if fr_obj.to_user != request.user:
            return Response({'error': 'Not authorised'}, status=status.HTTP_403_FORBIDDEN)

        if action == 'accept':
            fr_obj.accepted = True
            fr_obj.save()
            return Response({'message': 'Friend request accepted'})
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
