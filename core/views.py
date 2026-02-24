from django.shortcuts import render, redirect
from .books import books
from .bible_versions import versions
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, PasswordResetCode, Record, RecordPassage, RecordImage, WaitingList
from django.contrib import messages
from .utils import is_valid_email
from django.urls import reverse
from .forms import RecordNoteForm

API_BIBLE_BASE_URL = "https://rest.api.bible/v1"

@login_required
def home(request):

    return render(request, 'home.html')

def bible(request):

    context = {
        "books": books,
        "bible_versions": versions
    }
    return render(request, "bible/bible.html", context)

def waiting_list(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, "Email field is required")
            return redirect('waiting_list')
        
        email, created = WaitingList.objects.get_or_create(email=email)
        if created:
            messages.success(request, 'Your email has been added to our waiting list')
        else:
            messages.success(request, 'You already joined the waiting list')
        return redirect('waiting_list')


    return render(request, 'waiting_list.html')

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

def forgot_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        if not email or not is_valid_email(email):
            messages.error(request, 'Invalid email provided')
            return redirect('register_new_user')

        if not User.objects.filter(email=email).exists():
            messages.error(request, 'No user with that email exists')
            return redirect('forgot_password')
        
        user = User.objects.get(email=email)

        # delete old codes
        PasswordResetCode.objects.filter(user=user).delete()

        code = PasswordResetCode(user=user)
        code.save()
        
        user.send_password_reset_email(request, code.reset_id)

        return redirect(f"{reverse('forgot_password')}?password_reset_sent=True?email={email}")

    return render(request, 'auth/forgot_password.html')

def reset_password(request, reset_id):

    try:
        password_reset_code = PasswordResetCode.objects.get(reset_id=reset_id)

    except PasswordResetCode.DoesNotExist:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot_password')

    if request.method == "POST":

        # grab form data
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        passwords_have_error = False

        # validate form data
        if password != confirm_password:
            passwords_have_error = True
            messages.error(request, 'Passwords do not match')

        if len(password) < 5:
            passwords_have_error = True
            messages.error(request, 'Password must be at least 5 characters long')

        # check if link has expired
        if not password_reset_code.is_valid():
            passwords_have_error = True
            messages.error(request, 'The reset link has expired.')

            password_reset_code.delete()

        # reset user password if no issues were found
        if not passwords_have_error:
            user = password_reset_code.user
            user.set_password(password)
            user.save()

            password_reset_code.delete()

            messages.success(request, 'Password reset successfully. Please proceed to login')
            return redirect('login_user')
        
        return redirect('reset_user_password', reset_id=reset_id)

    return render(request, 'auth/reset_password.html')

@login_required
def create_record(request):

    user = request.user

    if request.method == "POST":
        title = request.POST.get('title')
        scriptures = request.POST.getlist('scriptures[]')
        
        form = RecordNoteForm(request.POST)
        if form.is_valid():
            record_content = form.cleaned_data['note']

        record = Record.objects.create(
            user = user,
            title = title,
            note = record_content
        )

        if scriptures:
            for scripture in scriptures:
                scripture = scripture.split('|')
                
                bible_version_id = scripture[0]
                chapter = scripture[1]
                verse = scripture[2]
                passage_content = scripture[3]

                RecordPassage.objects.create(
                    record = record,
                    bible_id = bible_version_id,
                    chapter_id = chapter,
                    verse_id = verse,
                    content = passage_content
                )

            record.number_of_passages = len(scriptures)
            record.save(update_fields=['number_of_passages'])

        messages.success(request, 'Record created successfully')
        return redirect('create_record')

    context = {
        "form": RecordNoteForm(),
        "books": books,
        "bible_versions": versions
    }
    return render(request, 'records/create_record.html', context)

@login_required
def user_records(request):

    records = Record.objects.filter(user=request.user)
    context = {
        'records': records
    }
    return render(request, 'records/user_records.html', context)