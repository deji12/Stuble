from django.shortcuts import render, redirect, get_object_or_404
from .books import books
from .bible_versions import versions
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, PasswordResetCode, Record, RecordPassage, Collection, WaitingList
from django.contrib import messages
from .utils import is_valid_email, superuser_required
from django.urls import reverse
from .forms import RecordNoteForm, EmailForm
from django.contrib.auth import update_session_auth_hash
from .tasks import send_bulk_emails

API_BIBLE_BASE_URL = "https://rest.api.bible/v1"


# ----------------------------------------------------------------
#                     LANDING PAGE & BIBLE
#-----------------------------------------------------------------

def landing(request):
    return render(request, 'index.html')

@login_required
def home(request):

    user = request.user
    latest_records = Record.objects.filter(user=user, is_deleted=False).order_by('-id')[:5]
    latest_passages = RecordPassage.objects.filter(
        record__user=user,
        record__is_deleted=False
    ).order_by('-id')[:5]
    
    context = {
        'recent_records': latest_records,
        'recent_passages': latest_passages,
        'user': user
    }
    return render(request, 'home.html', context)

def bible(request):

    context = {
        "books": books,
        "bible_versions": versions
    }
    return render(request, "bible/bible.html", context)

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




# ----------------------------------------------------------------
#                       WAITING LIST & MAILING
#-----------------------------------------------------------------

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
        return redirect('wait_list')


    return render(request, 'waiting_list.html')

@superuser_required
def send_out_bulk_email(request):

    if request.method == "POST":    
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            image = form.cleaned_data['image']
            button_text = form.cleaned_data['button_text']
            button_url = form.cleaned_data['button_url']

            # Prepare and send emails
            send_bulk_emails.delay(
                subject = subject, 
                message = message, 
                image_url = image if image else None, 
                button_text = button_text if button_text else None, 
                button_url = button_url if button_url else None
            )
                

            messages.success(request, "Emails sent out successfully")
            return redirect('/admin/core/waitinglist/')
        else:
            messages.error(request, "Invalid form input")  # Log the errors
            return redirect('/admin/core/waitinglist/')




# ----------------------------------------------------------------
#                       USER & AUTH
#-----------------------------------------------------------------

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

        email, created = WaitingList.objects.create(email=email)

        login(request, user)
        return redirect('dashboard')

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

            next = request.GET.get('next')
            return redirect(next or 'dashboard')

        messages.error(request, 'Invalid credentials provided')
        return redirect('login_user')

    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    return redirect('landing_page')

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
def edit_account(request):
    user = request.user
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        data_has_error = False
        
        # Validate required fields
        if not (first_name and last_name and email):
            messages.error(request, 'First name, last name and email are required')
            data_has_error = True
        
        # Validate email format
        if email and not is_valid_email(email):
            messages.error(request, 'You have entered an invalid email')
            data_has_error = True
        
        # Check if email is taken by another user
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, 'This email is already taken by another user')
                data_has_error = True
        
        # If changing password, validate current password
        if new_password or confirm_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect')
                data_has_error = True
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match')
                data_has_error = True
            elif len(new_password) < 6:
                messages.error(request, 'New password must be at least 6 characters long')
                data_has_error = True
        
        if data_has_error:
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
            return render(request, 'auth/edit_account.html', context)
        
        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # Update password if provided
        if new_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password has been updated successfully!')
        else:
            user.save()
            messages.success(request, 'Your account has been updated successfully!')
        
        return redirect('settings')
    
    # GET request - display form with current user data
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return render(request, 'auth/edit_account.html', context)

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Log the user out
        logout(request)
        # Delete the user
        user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('register_user')
    return redirect('edit_account')





# ----------------------------------------------------------------
#                       RECORDS
#-----------------------------------------------------------------

@login_required
def create_record(request):

    user = request.user

    if request.method == "POST":
        title = request.POST.get('title')
        scriptures = request.POST.getlist('scriptures[]')
        
        form = RecordNoteForm(request.POST)
        if form.is_valid():
            record_content = form.cleaned_data['note']
        else:
            messages.error(request, 'Invalid data entered')
            return redirect('create_record')

        record = Record.objects.create(
            user = user,
            title = title,
            note = record_content
        )

        user.number_of_records += 1

        if scriptures:
            for scripture in scriptures:
                scripture = scripture.split('|')
                
                bible_version_id = scripture[0]
                chapter = scripture[1]
                verse = scripture[2]
                passage_content = scripture[3]
                passage_formatted = scripture[4] # (KJV) Numbers 6:13

                RecordPassage.objects.create(
                    record = record,
                    bible_id = bible_version_id,
                    chapter_id = chapter,
                    verse_id = verse,
                    content = passage_content,
                    passage_formatted = passage_formatted
                )

            record.number_of_passages = len(scriptures)
            record.save(update_fields=['number_of_passages'])

            user.number_of_saved_passages += len(scriptures)

        user.save()

        messages.success(request, 'Record created successfully')
        return redirect('user_records')

    context = {
        "form": RecordNoteForm(),
        "books": books,
        "bible_versions": versions
    }
    return render(request, 'records/create_record.html', context)

@login_required
def user_records(request):
    records = Record.objects.filter(user=request.user).order_by('-created_at')
    
    search_query = request.GET.get('q', '')
    if search_query:
        records = records.filter(title__icontains=search_query)
    
    context = {
        'records': records,
        'search_query': search_query,
    }
    return render(request, 'records/user_records.html', context)

@login_required
def user_record(request, record_id):

    try:
        record = Record.objects.prefetch_related('record_passages').get(
            user=request.user, 
            id=record_id,
            is_deleted = False
        )
    except Record.DoesNotExist:
        messages.error(request, 'Record does not exist')
        return redirect('user_records')

    context = {
        'record': record,
        'passages': record.record_passages.all().order_by('-id')
    }
    return render(request, 'records/record.html', context)

@login_required
def edit_record(request, record_id):

    user = request.user

    try:
        record = Record.objects.prefetch_related('record_passages').get(
            user=user, 
            id=record_id,
            is_deleted = False
        )
    except Record.DoesNotExist:
        messages.error(request, 'Record does not exist') 
        return redirect('user_records')

    if request.method == "POST":
        title = request.POST.get('title')
        scriptures = request.POST.getlist('scriptures[]')
        
        form = RecordNoteForm(request.POST)
        if form.is_valid():
            record_content = form.cleaned_data['note']
        else:
            messages.error(request, 'Invalid data entered')
            return redirect('edit_record', record_id=record_id)

        if title != record.title:
            record.title = title


        # if passages do not come in, it means they were deleted from frontend
        record_passages = record.record_passages.all()
        number_of_passages = record_passages.count()
        record_passages.delete()

        user.number_of_saved_passages -= number_of_passages

        if scriptures:
            for scripture in scriptures:
                scripture = scripture.split('|')
                
                bible_version_id = scripture[0]
                chapter = scripture[1]
                verse = scripture[2]
                passage_content = scripture[3]
                passage_formatted = scripture[4] # (KJV) Numbers 6:13

                RecordPassage.objects.create(
                    record = record,
                    bible_id = bible_version_id,
                    chapter_id = chapter,
                    verse_id = verse,
                    content = passage_content,
                    passage_formatted = passage_formatted
                )
            user.number_of_saved_passages += len(scriptures)

            record.note = record_content
            record.number_of_passages = len(scriptures)
        
        record.save()
        user.save()

        messages.success(request, 'Record updated successfully')
        return redirect('user_record', record_id=record_id)

    form = RecordNoteForm(instance=record)

    context = {
        'form': form,
        'record': record,
        'passages': record.record_passages.all(),
        "books": books,
        "bible_versions": versions
    }
    return render(request, 'records/edit_record.html', context)
    
@login_required
def delete_record(request, record_id):

    user = request.user
    try:
        record = Record.objects.get(
            user=user, 
            id=record_id,
            is_deleted = False
        )
        record.is_deleted = True
        record.save()

        # make sure to update the number of passages
        number_of_saved_passages = record.record_passages.all().count()
        user.number_of_saved_passages -= number_of_saved_passages
        user.save()

        messages.success(request, 'Record deleted successfully')
    
    except Record.DoesNotExist:
        messages.error(request, 'Record does not exist')
        
    return redirect('user_records')





# ----------------------------------------------------------------
#                       COLLECTION
#-----------------------------------------------------------------

@login_required
def user_collections(request):

    user = request.user

    records = Record.objects.filter(user=user, is_deleted=False)
    collections = Collection.objects.filter(user=user, is_deleted=False)

    context = {
        'user_records': records,
        'collections': collections
    }
    return render(request, 'collections/user_collections.html', context)

@login_required
def create_collection(request):

    user = request.user
    
    if request.method == 'POST':
        collection_title = request.POST.get('collection_title')
        record_ids  = request.POST.getlist('records')

        if not collection_title:
            messages.error(request, 'Collection name is required')
            return redirect('user_collections')

        
        new_collection = Collection.objects.create(
            title=collection_title,
            user=user  
        )

        if record_ids:
            # Optional: Filter to ensure records belong to the user
            records = Record.objects.filter(
                id__in=record_ids,
                user=request.user
            )
            new_collection.records.set(records)  

        user.number_of_collections += 1
        user.save(updated_fields=['number_of_collections'])
        
        messages.success(request, 'Collection created successfully')
        return redirect('user_collections')
    
@login_required
def edit_collection(request):

    user = request.user
    
    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        collection_title = request.POST.get('title')
        record_ids = request.POST.getlist('records')
        
        if not collection_title:
            messages.error(request, 'Collection name is required')
            return redirect('user_collections')
        
        try:
            collection = Collection.objects.get(id=collection_id, user=user)
            
            collection.title = collection_title
            
            if record_ids:
                # Filter to ensure records belong to the user
                records = Record.objects.filter(
                    id__in=record_ids,
                    user=user
                )
                collection.records.set(records)
            else:
                # If no records selected, clear the collection
                collection.records.clear()
            
            collection.save()
            messages.success(request, 'Collection updated successfully')
            
        except Collection.DoesNotExist:
            messages.error(request, 'Collection not found')
            
        return redirect('user_collections')
    
@login_required
def delete_collection(request):

    user = request.user

    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        
        try:
            collection = Collection.objects.get(id=collection_id, user=user)
            collection.is_deleted = True
            collection.save(update_fields=['is_deleted'])

            user.number_of_collections -= 1
            user.save(updated_fields=['number_of_collections'])
            messages.success(request, 'Collection deleted successfully')
        except Collection.DoesNotExist:
            messages.error(request, 'Collection not found')
    
    return redirect('user_collections')

@login_required
def user_collection(request, collection_id):

    user = request.user

    try:
        collection = Collection.objects.get(id=collection_id, user=user)
    except Collection.DoesNotExist:
        messages.error(request, 'Collection does not exist')

    records = Record.objects.filter(user=user, is_deleted=False)
    

    context = {
        'collection': collection,
        'user_records': records,
    }

    return render(request, 'collections/user_collection.html', context)