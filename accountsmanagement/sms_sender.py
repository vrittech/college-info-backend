from django.conf import settings
import  requests
from django.conf import settings
from django.core.mail import send_mail

SMS_KEY = settings.SMS_KEY_PASSWORD

def SendSms(message,contact,otp):
    message = message + " " + str(otp)
    sms_api = f"https://sms.vrittechnologies.com/smsapi/index?key={SMS_KEY}&contacts={contact}&senderid=SMSBit&msg={message}&responsetype=json"
    print(sms_api)
    response = requests.get(sms_api)
    print(response.json)
    return True

def ContactMe(user_email,user_phone,full_name,subject,message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]
    message = f"A client  {full_name}, {user_email},mobile number {user_phone} Try to contact you "+message
    send_mail(subject, '', email_from, recipient_list,html_message=message)
    return True
