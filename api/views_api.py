from datetime import date, timedelta
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Hobby, FriendRequest
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    HobbySerializer,
    FriendRequestSerializer
)


# views_api.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_friends_view(request):
    friends_qs = request.user.friends()
    serializer = UserSerializer(friends_qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Returns the currently authenticated user's details.
    """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def hobby_list_create_view(request):
    """
    Handles fetching all hobbies or creating a new one.
    """
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
    """
    Fetch a paginated list of users, optionally filtered by age range,
    ordered by how many hobbies they have in common with the logged-in user.
    """
    today = date.today()
    min_age_str = request.GET.get('min_age')
    max_age_str = request.GET.get('max_age')
    page_str = request.GET.get('page', 1)

    users_qs = CustomUser.objects.exclude(pk=request.user.pk)

    # Filter by minimum age
    if min_age_str:
        try:
            min_age = int(min_age_str)
            min_birth_date = today - timedelta(days=min_age * 365)
            users_qs = users_qs.filter(date_of_birth__lte=min_birth_date)
        except ValueError:
            pass

    # Filter by maximum age
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
    paginator = Paginator(users_qs, 10)  # Show 10 users per page
    try:
        page_obj = paginator.get_page(page_str)
    except ValueError:
        return Response({'error': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)

    # We want to serialize each user with their common_hobbies_count
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
    """
    Fetch or update a specific user's details (including optional pass/username).
    """
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'GET':
        serializer = UserSerializer(user_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.id != user_obj.id:
            return Response(
                {'error': 'You cannot edit another user’s profile.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserUpdateSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def friend_request_view(request):
    """
    Handle friend requests.
    - GET: Return friend requests relevant to current user (pending).
    - POST: Send a friend request.
    - PUT: Accept a friend request.
    """
    if request.method == 'GET':
        pending_requests = FriendRequest.objects.filter(
            to_user=request.user,
            accepted=False
        )
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        to_user_id = request.data.get('to_user_id')
        from_user = request.user

        if not to_user_id:
            return Response({'error': 'No recipient provided'}, status=status.HTTP_400_BAD_REQUEST)

        if from_user.pk == int(to_user_id):
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        to_user = get_object_or_404(CustomUser, pk=to_user_id)
        fr, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({'error': 'Friend request already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)

    elif request.method == 'PUT':
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')

        if not friend_request_id or not action:
            return Response({'error': 'Missing friend request ID or action'}, status=status.HTTP_400_BAD_REQUEST)

        fr_obj = get_object_or_404(FriendRequest, pk=friend_request_id)

        if fr_obj.to_user != request.user:
            return Response({'error': 'Not authorised'}, status=status.HTTP_403_FORBIDDEN)

        if action == 'accept':
            fr_obj.accepted = True
            fr_obj.save()
            return Response({'message': 'Friend request accepted'})
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
