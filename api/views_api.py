# api/views_api.py

from datetime import date, timedelta
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def hobby_list_create_view(request):
    """
    GET: Return all hobbies as JSON.
    POST: Create a new hobby.
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
    Returns a JSON list of other users, sorted by the number of hobbies in common with the current user.
    Allows age filtering (min_age, max_age).
    Includes pagination (10 per page).
    """
    current_user = request.user
    min_age_str = request.GET.get('min_age')
    max_age_str = request.GET.get('max_age')
    page_str = request.GET.get('page', '1')

    users_qs = CustomUser.objects.exclude(pk=current_user.pk).annotate(
        common_hobbies_count=Count('hobbies', filter=Q(hobbies__in=current_user.hobbies.all()))
    ).order_by('-common_hobbies_count')

    today = date.today()
    # Filter by min_age
    if min_age_str:
        try:
            min_age = int(min_age_str)
            min_birth_date = today - timedelta(days=min_age * 365)
            users_qs = users_qs.filter(date_of_birth__lte=min_birth_date)
        except ValueError:
            pass

    # Filter by max_age
    if max_age_str:
        try:
            max_age = int(max_age_str)
            max_birth_date = today - timedelta(days=max_age * 365)
            users_qs = users_qs.filter(date_of_birth__gte=max_birth_date)
        except ValueError:
            pass

    # Pagination
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
    """
    GET: Returns user details (including hobbies).
    PUT: Updates user’s profile data (name, email, date_of_birth, hobbies).
    """
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'GET':
        serializer = UserSerializer(user_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Use a separate serializer for updates
        serializer = UserUpdateSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()

            # If you want to handle hobby creation by name here, do so:
            if 'hobbies' not in request.data:
                # If you don’t send the hobbies list, skip
                pass
            else:
                # Here, request.data['hobbies'] might be a list of IDs or names
                # if you prefer them by name, you'd do something like:
                # new_hobbies = request.data['hobbies']
                # hobby_objs = []
                # for h_name in new_hobbies:
                #     hobby_obj, _ = Hobby.objects.get_or_create(name=h_name)
                #     hobby_objs.append(hobby_obj)
                # updated_user.hobbies.set(hobby_objs)

                pass

            return Response({'message': 'User updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def friend_request_view(request):
    """
    POST: Creates a new friend request (from current user to 'to_user_id').
    PUT: Accepts a friend request if current user is the recipient (action='accept').
    """
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
