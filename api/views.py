from __future__ import annotations
from typing import Any, Dict, List, Optional
import json
from datetime import date, timedelta

from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Count, Q

# Import forms and models
from .forms import SignupForm, SigninForm, ProfileUpdateForm
from .models import CustomUser, Hobby, FriendRequest


def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Server-side rendered signup using Django forms.
    POST: Creates a new user if form is valid.
    GET: Renders signup form.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # After creation, we can either auto-login or redirect to login
            return redirect('login')
        return render(request, 'api/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'api/signup.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Server-side rendered login using Django's authentication.
    POST: Authenticates user if credentials are valid.
    GET: Renders login form.
    """
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


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and redirects to login page.
    """
    logout(request)
    return redirect('login')


@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    """
    The main entry point for the Vue SPA.
    Only accessible if user is authenticated.
    """
    return render(request, 'api/spa/index.html', {})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    Server-side form to allow user to update profile (including hobbies and date_of_birth).
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in if password changed
            return redirect('/')  # or redirect to a "profile updated" page
        return render(request, 'api/profile.html', {'form': form})
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'api/profile.html', {'form': form})


@login_required
@csrf_exempt
def hobbies_view(request: HttpRequest) -> HttpResponse:
    """
    Ajax-based hobby management:
      - GET: Return all hobbies (JSON).
      - POST: Create a new hobby if it doesn't exist.
    """
    if request.method == 'GET':
        all_hobbies = Hobby.objects.all().values('id', 'name')
        return JsonResponse({'hobbies': list(all_hobbies)})

    elif request.method == 'POST':
        data = json.loads(request.body)
        hobby_name = data.get('hobby_name')
        if not hobby_name:
            return JsonResponse({'error': 'No hobby name provided'}, status=400)
        hobby_obj, created = Hobby.objects.get_or_create(name=hobby_name)
        return JsonResponse({
            'message': 'Hobby created' if created else 'Hobby already exists',
            'id': hobby_obj.id,
            'name': hobby_obj.name,
        }, status=201 if created else 200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def user_list_view(request: HttpRequest) -> HttpResponse:
    """
    Returns a JSON list of users sorted by the number of hobbies in common with the current user.
    Allows age filtering (min_age, max_age).
    Includes pagination (10 per page).
    """
    current_user: CustomUser = request.user  # type: ignore
    page_str = request.GET.get('page', '1')
    min_age_str = request.GET.get('min_age')
    max_age_str = request.GET.get('max_age')

    # Base queryset: exclude current user
    users_qs = CustomUser.objects.exclude(pk=current_user.pk).annotate(
        common_hobbies_count=Count('hobbies', filter=Q(hobbies__in=current_user.hobbies.all()))
    ).order_by('-common_hobbies_count')

    # Filter by age range if provided
    today = date.today()
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

    paginator = Paginator(users_qs, 10)
    page_obj = paginator.get_page(page_str)

    # Build data
    users_data: List[Dict[str, Any]] = []
    for user in page_obj:
        users_data.append({
            'id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'common_hobbies': getattr(user, 'common_hobbies_count', 0),
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None
        })

    return JsonResponse({
        'users': users_data,
        'page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
    })


@login_required
@csrf_exempt
def user_detail_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    GET: Returns user details (including hobbies).
    PUT: Updates user’s profile data (name, email, date_of_birth, hobbies).
         This can be used by the SPA if you prefer, or rely on profile_view for SSR.
    """
    user_obj = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'GET':
        return JsonResponse({
            'id': user_obj.pk,
            'username': user_obj.username,
            'name': user_obj.first_name,
            'email': user_obj.email,
            'date_of_birth': user_obj.date_of_birth.isoformat() if user_obj.date_of_birth else None,
            'hobbies': [h.name for h in user_obj.hobbies.all()],
        })

    elif request.method == 'PUT':
        data = json.loads(request.body)
        user_obj.first_name = data.get('name', user_obj.first_name)
        user_obj.email = data.get('email', user_obj.email)

        dob_str = data.get('date_of_birth')
        if dob_str:
            user_obj.date_of_birth = dob_str
        user_obj.save()

        # Update hobbies
        new_hobbies = data.get('hobbies', [])
        hobby_objs = []
        for h_name in new_hobbies:
            hobby_obj, _ = Hobby.objects.get_or_create(name=h_name)
            hobby_objs.append(hobby_obj)
        user_obj.hobbies.set(hobby_objs)

        return JsonResponse({'message': 'User updated successfully'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
@csrf_exempt
def friend_request_view(request: HttpRequest) -> HttpResponse:
    """
    POST: Creates a new friend request (from current user to 'to_user_id').
    PUT: Accepts a friend request (action='accept') if current user is the recipient.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        to_user_id = data.get('to_user_id')
        from_user: CustomUser = request.user  # type: ignore

        if from_user.pk == to_user_id:
            return JsonResponse({'error': 'Cannot send friend request to yourself'}, status=400)

        to_user = get_object_or_404(CustomUser, pk=to_user_id)
        fr, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return JsonResponse({'error': 'Friend request already exists'}, status=400)
        return JsonResponse({'message': 'Friend request sent'}, status=201)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        friend_request_id = data.get('friend_request_id')
        action = data.get('action')

        fr_obj = get_object_or_404(FriendRequest, pk=friend_request_id)
        if fr_obj.to_user != request.user:
            return JsonResponse({'error': 'Not authorised'}, status=403)

        if action == 'accept':
            fr_obj.accepted = True
            fr_obj.save()
            return JsonResponse({'message': 'Friend request accepted'}, status=200)

        return JsonResponse({'error': 'Invalid action'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
