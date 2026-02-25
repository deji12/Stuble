from django.forms import ModelForm
from .models import Record
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class RecordNoteForm(ModelForm):
    class Meta:
        model = Record
        fields = ['note']

class EmailForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        label="Email Subject",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the subject'
        })
    )
    image = forms.URLField(
        label="Image URL",
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter an image URL (optional)'
        })
    )
    message = forms.CharField(
        label="Email Message",
        widget=CKEditor5Widget(attrs={
            'config_name': 'default'  # Use the CKEditor config defined in settings.py
        })
    )

    button_text = forms.CharField(
        max_length=255,
        label="Button Tex",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the buton text'
        })
    )

    button_url = forms.CharField(
        max_length=255,
        label="Button url",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the button url'
        })
    )