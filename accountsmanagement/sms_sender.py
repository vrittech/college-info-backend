from django.conf import settings
import  requests
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

SMS_KEY = settings.SMS_KEY_PASSWORD

def SendSms(message,contact,otp):
    message = message + " " + str(otp)
    sms_api = f"https://sms.vrittechnologies.com/smsapi/index?key={SMS_KEY}&contacts={contact}&senderid=SMSBit&msg={message}&responsetype=json"
    print(sms_api)
    response = requests.get(sms_api)
    print(response.json)
    return True



def ContactMe(user_email,full_name, user_phone,  subject, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]

    # Render HTML email template with dynamic data
    html_content = render_to_string('contact_email.html', {
        'full_name': full_name,
        'user_email': user_email,
        'user_phone': user_phone,
        'message': message
    })

    # Generate plain text version (fallback for email clients that don't support HTML)
    text_content = strip_tags(html_content)

    # Create email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Plain text content
        from_email=email_from,
        to=recipient_list
    )

    # Attach HTML content
    email.attach_alternative(html_content, "text/html")

    # Send email
    email.send()

    return True
