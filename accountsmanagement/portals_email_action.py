from django.conf import settings
from django.core.mail import send_mail
import time
import asyncio

async def MailAfterPortalCreated(instance):
    subject=f"Greeting!!! you have succesfully added a  new portal {instance.name} "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [instance.requested_by_email]
    message = f"you have request for portal {instance.name} , this will can take while for approved , we will inform you if portal verified"
    send_mail(subject, message, email_from, recipient_list)

async def MailAfterPortalVerify(instance):
    subject=f"Greeting!!! you were added {instance.name} which is succesfully verified"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [instance.requested_by_email]
    message = f"you were request for portal {instance.name} , which is succesfully verified , you can now create publisher"
    send_mail(subject, message, email_from, recipient_list)