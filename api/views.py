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
