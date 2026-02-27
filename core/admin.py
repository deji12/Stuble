from django.contrib import admin
from .models import User, Record, RecordImage, RecordPassage, WaitingList, Collection, PasswordResetCode
from import_export.admin import ImportExportModelAdmin
from .forms import EmailForm
from django.template.response import TemplateResponse

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

@admin.register(Record)
class RecordAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'user', 'number_of_passages', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at', 'user')
    search_fields = ('title', 'user__email')
    ordering = ('-created_at',)

@admin.register(RecordPassage)
class RecordPassageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'record', 'bible_id', 'chapter_id', 'verse_id', 'passage_formatted')
    list_filter = ('bible_id',)
    search_fields = ('bible_id', 'chapter_id', 'passage_formatted')
    ordering = ('record', 'bible_id', 'chapter_id')

@admin.register(RecordImage)
class RecordImageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'record', 'image')
    list_filter = ('record',)
    search_fields = ('record__title',)

@admin.register(WaitingList)
class WaitingListAdmin(ImportExportModelAdmin):
    list_display = ('id', 'email', 'created_when')
    search_fields = ('email',)
    ordering = ('-created_when',)
    actions = ["send_custom_email"]

    def send_custom_email(self, request, queryset):
        """
        Send a custom email to selected recipients with dynamic subject and message.
        """

        form = EmailForm()
        
        return TemplateResponse(
            request, 
            "admin/send_email_form.html", 
            {"form": form, "recipients": queryset}
        )
    
    send_custom_email.short_description = "Send email to selected users"

@admin.register(Collection)
class CollectionAdmin(ImportExportModelAdmin):
    list_display = ('title', 'id', 'user', 'is_deleted', 'created_at')
    list_filter = ('user', 'created_at', 'last_updated_at', 'is_deleted')
    search_fields = ('title', 'user__email')
    ordering = ('title',)

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'reset_id', 'created_when')
    search_fields = ('user__email',)
    ordering = ('-created_when',)