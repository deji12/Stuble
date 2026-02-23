from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django_quill.fields import QuillField
from cloudinary.models import CloudinaryField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, help_text="The user unique email address.")
    first_name = models.CharField(max_length=30, help_text="User first name.")
    last_name = models.CharField(max_length=30, help_text="User first name.")

    is_staff =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, help_text="Indicates whether the user has all admin permissions. Defaults to False.")
    is_active = models.BooleanField(default=True, help_text="Indicates whether the user account is active. Defaults to False and user needs to verify email on signup before it can be set to True.")
    
    last_used_ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="The last IP address used by the user.")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="The date and time when the user joined.")
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def send_password_reset_email(self, request, reset_id):
        password_reset_url = reverse('reset_user_password', kwargs={'reset_id': reset_id})
        full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
        
        email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
        email_message = EmailMessage(
            'Reset your password',
            email_body,
            settings.EMAIL_HOST_USER,
            [self.email]
        )
        
        email_message.fail_silently = True
        email_message.send()

    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True,editable=False)
    created_when = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Password reset for {self.user.username} at {self.created_when}'
    
    def is_valid(self):
        expiration_time = self.created_when + timezone.timedelta(minutes=10)
        return timezone.now() < expiration_time
    
class Record(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='records')
    title = models.CharField(max_length=100)
    note = QuillField()
    number_of_images = models.PositiveIntegerField(default=0)
    number_of_passages = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class RecordPassage(models.Model):
    
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='record_passages')
    bible_id = models.CharField(max_length=10)
    chapter_id = models.CharField(max_length=10)
    verse_id = models.CharField(max_length=10, default='', null=True, blank=True)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.bible_id} {self.chapter_id}:{self.verse_id}" 

class RecordImage(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='record_images')
    image = CloudinaryField(folder=f'{settings.CLOUDINARY_MEDIA_PREFIX_URL}/record_images/', blank=True, null=True)

class Collection(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='collections')
    records = models.ManyToManyField(Record)

class WaitingList(models.Model):
    
    email = models.EmailField()

    def __str__(self):
        return self.email