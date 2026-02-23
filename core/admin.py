from django.contrib import admin
from .models import User, Record, RecordImage, RecordPassage, WaitingList

admin.site.register(WaitingList)
admin.site.register(User)
admin.site.register(Record)
admin.site.register(RecordPassage)
admin.site.register(RecordImage)
