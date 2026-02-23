from django.forms import ModelForm
from .models import Record

class RecordNoteForm(ModelForm):
    class Meta:
        model = Record
        fields = ['note']