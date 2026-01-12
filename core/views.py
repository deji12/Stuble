from django.shortcuts import render, redirect
from .books import books
from .bible_versions import versions
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from .utils import is_valid_email

API_BIBLE_BASE_URL = "https://rest.api.bible/v1"

@login_required
def home(request):

    return render(request, 'home.html')

def bible(request):

    context = {
        "books": books,
        "bible_versions": versions
    }
    return render(request, "bible.html", context)

@require_GET
def get_chapter_passage(request):
    bible_id = request.GET.get("bibleId")
    chapter_id = request.GET.get("chapterId")
    verse_id = request.GET.get("verseId")

    if not bible_id or not chapter_id:
        return JsonResponse(
            {"error": "bibleId and chapterId are required"},
            status=400
        )

    if not verse_id:
        url = f"{API_BIBLE_BASE_URL}/bibles/{bible_id}/passages/{chapter_id}"
    else:
        url = f"{API_BIBLE_BASE_URL}/bibles/{bible_id}/verses/{chapter_id}.{verse_id}"

    headers = {
        "api-key": settings.API_BIBLE_KEY    
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {
                "error": "Failed to fetch passage",
                "detail": str(e),
            },
            status=502
        )

    return JsonResponse(response.json(), safe=False)

def register(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password')

        data_has_error = False
        if not (first_name and last_name and email and password):
            messages.error(request, 'All fields are required')

        if not len(password) > 5:
            data_has_error = True
            messages.error(request, 'Password must be at least 5 characters long')

        if not is_valid_email(email):
            data_has_error = True
            messages.error(request, 'You have entered an invalid email')

        if User.objects.filter(email=email).exists():
            data_has_error = True
            messages.error(request, 'A user with this email exists')
        
        if data_has_error:

            context = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
            return render(request, 'auth/register.html', context)

        user = User.objects.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password
        )

        login(user)
        return redirect('home')

    return render(request, 'auth/register.html')

def login_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password):
            messages.error(request, 'Username and password are required')
            return redirect('login_user')
        
        user = authenticate(request=request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid credentials provided')
        return redirect('login_user')

    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')