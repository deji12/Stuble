from celery import shared_task
from .models import WaitingList
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging
from stuble.celery import app

logger = logging.getLogger(__name__)

@app.task(name='send_bulk_emails')
def send_bulk_emails(
        subject, 
        message, 
        image_url=None, 
        button_text=None, 
        button_url=None
    ):

    logger.info("send_bulk_emails STARTED")
    
    recipients = WaitingList.objects.values_list('email', flat=True)
    # recipients = ['ptutsi@proton.me', 'theprotonguy@yahoo.com']

    email_template = 'admin/mass_email_template.html'
    email_data = {
        "subject": subject,
        "content": message,
        'image': image_url,
        'button_text': button_text,
        'button_url': button_url,
    }
    email_body = render_to_string(email_template, email_data)

    email = EmailMessage(
        subject,
        email_body,
        settings.EMAIL_HOST_USER,
        bcc = recipients
    )
    email.fail_silently = True
    email.content_subtype = 'html'
    email.send()

    logger.info("send_bulk_emails FINISHED")
    return f"Sent out {recipients.count()} emails"