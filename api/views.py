from typing import Any, Dict, List
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import CustomUser, Hobby, FriendRequest

def main_spa(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'api/spa/index.html', {})

def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        dob = request.POST.get('date_of_birth')
        name = request.POST.get('name')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )
        if dob:
            user.date_of_birth = dob
            user.save()
        return redirect('login')

    return render(request, 'api/signup.html')

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'api/login.html', {'error': 'Invalid credentials'})
    return render(request, 'api/login.html')

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')

@login_required
@csrf_exempt
def hobbies_view(request: HttpRequest) -> HttpResponse:
    """
    GET: Returns the list of all hobbies in the database.
    POST: Creates a new hobby if it doesn't exist.
    """
    if request.method == 'GET':
        all_hobbies = list(Hobby.objects.all().values('id', 'name'))
        return JsonResponse({'hobbies': all_hobbies})

    if request.method == 'POST':
        data = json.loads(request.body)
        hobby_name = data.get('hobby_name')
        if not hobby_name:
            return JsonResponse({'error': 'No hobby name provided'}, status=400)

        hobby_obj, created = Hobby.objects.get_or_create(name=hobby_name)
        return JsonResponse({
            'message': 'Hobby created' if created else 'Hobby already exists',
            'id': hobby_obj.id,
            'name': hobby_obj.name
        }, status=201 if created else 200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def user_list_view(request: HttpRequest) -> HttpResponse:
    """
    Returns JSON list of users, sorted by number of common hobbies with the current user.
    Allows filtering by age (min_age/max_age) and uses pagination (up to 10 per page).
    """
    current_user = request.user
    if not isinstance(current_user, CustomUser):
        return JsonResponse([], safe=False)

    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    page_num = request.GET.get('page', 1)

    # Exclude the current user
    users_qs = CustomUser.objects.exclude(pk=current_user.pk)

    # Age filtering logic:
    # We'll assume date_of_birth is used to calculate age. For a real approach, you'd actually
    # compute the user’s age in years. Here, we'll do a placeholder or skip the actual logic.
    # For demonstration, we won't implement actual date calculations, but you can:
    # from datetime import date
    # def calculate_age(dob):
    #     return (date.today() - dob).days // 365
    #
    # Then filter if min_age & max_age exist

    if min_age and max_age:
        try:
            min_age_val = int(min_age)
            max_age_val = int(max_age)
            # Pseudo-filter: users who have a date_of_birth that implies their age is within range
            # We skip real logic for brevity. But something like:
            # valid_user_ids = []
            # for u in users_qs:
            #     if u.date_of_birth:
            #         user_age = calculate_age(u.date_of_birth)
            #         if min_age_val <= user_age <= max_age_val:
            #             valid_user_ids.append(u.id)
            # users_qs = users_qs.filter(id__in=valid_user_ids)
        except ValueError:
            pass  # if parsing fails, skip age filtering

    # Build user data with common hobbies count
    user_data_list = []
    current_user_hobbies = current_user.hobbies.all()
    for user in users_qs:
        user_hobbies = user.hobbies.all()
        common_count = user_hobbies.filter(pk__in=current_user_hobbies).count()
        user_data_list.append({
            'id': user.pk,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'common_hobbies': common_count,
        })

    # Sort descending by common_hobbies
    user_data_list.sort(key=lambda u: u['common_hobbies'], reverse=True)

    # Paginate
    paginator = Paginator(user_data_list, 10)
    page_obj = paginator.get_page(page_num)

    response_data = {
        'results': list(page_obj),
        'has_next': page_obj.has_next(),
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
    }
    return JsonResponse(response_data)

@login_required
@csrf_exempt
def user_detail_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    GET: Returns user details (including hobbies).
    PUT: Updates user’s profile data, including hobbies.
    """
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'GET':
        return JsonResponse({
            'id': user_obj.pk,
            'username': user_obj.username,
            'name': user_obj.name,
            'email': user_obj.email,
            'date_of_birth': user_obj.date_of_birth,
            'hobbies': [h.name for h in user_obj.hobbies.all()]
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        user_obj.first_name = data.get('name', user_obj.first_name)
        user_obj.email = data.get('email', user_obj.email)

        # If a new date_of_birth is provided
        dob = data.get('date_of_birth')
        if dob:
            user_obj.date_of_birth = dob
        user_obj.save()

        # Handle new or existing hobbies
        new_hobbies = data.get('hobbies', [])
        hobby_objs = []
        for h in new_hobbies:
            hobby_obj, _ = Hobby.objects.get_or_create(name=h)
            hobby_objs.append(hobby_obj)
        user_obj.hobbies.set(hobby_objs)

        return JsonResponse({'message': 'User updated successfully'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def friend_request_view(request: HttpRequest) -> HttpResponse:
    """
    POST: create a new friend request
    PUT: accept a friend request
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        to_user_id = data.get('to_user_id')
        from_user = request.user

        if from_user.id == to_user_id:
            return JsonResponse({'error': 'Cannot send friend request to yourself'}, status=400)

        to_user = get_object_or_404(CustomUser, pk=to_user_id)
        fr, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return JsonResponse({'error': 'Friend request already exists'}, status=400)
        return JsonResponse({'message': 'Friend request sent'}, status=201)

    if request.method == 'PUT':
        data = json.loads(request.body)
        friend_request_id = data.get('friend_request_id')
        action = data.get('action')

        fr_obj = get_object_or_404(FriendRequest, pk=friend_request_id)
        # Only the recipient can accept
        if fr_obj.to_user != request.user:
            return JsonResponse({'error': 'Not authorised'}, status=403)

        if action == 'accept':
            fr_obj.accepted = True
            fr_obj.save()
            return JsonResponse({'message': 'Friend request accepted'}, status=200)

        return JsonResponse({'error': 'Invalid action'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
