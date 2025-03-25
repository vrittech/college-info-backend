# from django.shortcuts import render
from rest_framework import generics, status, viewsets, response
from .serializers import EmailNumberSerializer,PasswordNumberSerializer, CustomPasswordResetSerializer, TokenValidationSerializer,ContactMeSerializer,EmailResetSerializer,EmailChangeGetOtpSerializer
from accounts.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from .serializers import CustomChangePasswordSerializer

# from booking.models import DestinationBook

# from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .sms_sender import SendSms,ContactMe
from django.db.models import Q
from django.core.cache import cache

import random
import string

otp_time_expired = 600
site_f  = "https://collegeinfocrmm.netlify.com" #http://localhost:4200"#"https://dev-lims.netlify.app"#"https://lims.dftqc.gov.np"

class EmailCheckView(generics.GenericAPIView):

    def generate_otp(self,user):
        # Generate a random 6-digit OTP
        user = str(user)
        return user[0]+''.join(random.choices(string.digits, k=4)) + user[-1]
    
    serializer_class = EmailNumberSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = CustomUser.objects.filter(Q(email=email) | Q(phone = email)).first()
        if user:
        
            otp = self.generate_otp(user.id)

            reset_verification = "verification"
            subject = 'College Info Nepal OTP'
            if '@' in email:
                email = user.email
                sendMail(email, otp,subject,reset_verification)
            else:
                SendSms(contact=email,otp=otp,message=subject)
          
            cache_key = f"password_reset_otp_{user.id}"
        
            cache.set(cache_key, otp, timeout=otp_time_expired)

            return response.Response(
                {
                "message": "otp has been sent to your email address"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class EmailChangeGetOtpView(generics.GenericAPIView):
    def generate_otp(self,user):
        # Generate a random 6-digit OTP
        # return "123456"
        user = str(user)
        return user[0]+''.join(random.choices(string.digits, k=4)) + user[-1]
    
    serializer_class = EmailChangeGetOtpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = CustomUser.objects.filter(Q(email=email) | Q(phone = email)).first()
        if user:
        
            otp = self.generate_otp(user.id)

            reset_verification = "reset_email"
            subject = 'Pacific OTP'
            if '@' in email:
                email = user.email
                sendMail(serializer.data["second_email"], otp,subject,reset_verification)
            else:
                SendSms(contact=email,otp=otp,message=subject)
          
            cache_key = f"email_reset_otp_{user.id}"
            cache.set(cache_key, otp, timeout=otp_time_expired)

            return response.Response(
                {
                "message": f"otp has been sent to your email address {serializer.data['second_email']} "
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class CustomPasswordResetView(generics.GenericAPIView):
    serializer_class = CustomPasswordResetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
     
        user = CustomUser.objects.get(Q(email = serializer.data.get('email')) | Q(phone = serializer.data.get('email')))
        if serializer.validated_data.get('token_validate') == True:
            user.password = serializer.data.get('password')
            user.save()
            message = "Password Reset Complete"
            stat = status.HTTP_200_OK
            print(" password save ")
        else:
            message = "Password Reset not Completed"
            stat = status.HTTP_400_BAD_REQUEST
            print("password not save")

        return response.Response(
            {"message": message},
            status=stat,
        )

class EmailResetView(generics.GenericAPIView):
    serializer_class = EmailResetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
     
        user = CustomUser.objects.get(Q(email = serializer.data.get('email')))
        if not check_password(serializer.data.get('password'),user.password):
            message = "password does not match"
            stat = status.HTTP_200_OK
        if serializer.validated_data.get('token_validate') == True:
            print("validate  data")
            user.email = serializer.data.get('second_email')
            user.save()
            message = "Email Reset Complete"
            stat = status.HTTP_200_OK
            print(" Email Reset save ")
        else:
            message = "Email Can Not reset"
            stat = status.HTTP_400_BAD_REQUEST
            print("Email Reset not save")

        return response.Response(
            {"message": message},
            status=stat,
        )
    

class VerifyUserPasswordToken(generics.GenericAPIView):
    serializer_class = TokenValidationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)

        # ✅ OTP is already verified in the serializer, now update `is_verified`
        email = serializer.validated_data.get("email")
        user = CustomUser.objects.filter(Q(email=email) | Q(phone=email)).first()

        if user and not user.is_verified:  # Only update if it's False
            user.is_verified = True
            user.save()

        return response.Response(
            {
                "message": "OTP verified successfully, your account is now verified!",
                'data': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SendEmailVerificationLink(APIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({
                'detail': 'User with this email does not exist.',
            }, status=status.HTTP_400_BAD_REQUEST)

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Send the token via email
        subject = 'Email Verification Token'
        verify_url = f"{site_f}/user-verification-success?pk={encoded_pk}&token={token}"
        subject = 'Email Verification Link '
        reset_verification = "verification"
        sendMail(email,verify_url,subject,reset_verification)

        return Response({
            'detail': 'Email verification'})


def sendMail(email, otp, subject, reset_verification):
    """
    Sends an email for account verification or password reset with OTP & Verify Button.
    """

    if reset_verification == "verification":
        body = f"""<body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="https://collegeinfoapi.vrittechnologies.com/media/gallery/images/College_Info_Nepal.png" alt="College Info Nepal Logo" width="150" style="display: block; margin: 0 auto;">
                        <p style="color: #1CA3FD; font-weight: 600; font-size: 18px; margin-top: 20px;">College Info Nepal</p>
                        <p style="color: #1CA3FD; font-weight: 600; font-size: 18px; margin-top: 20px;">Please Verify Your Account</p>
                        <p style="text-align: center; font-weight: 400;">Use the OTP code below to verify your account:</p>
                        <div style="font-size: 32px; font-weight: bold; letter-spacing: 15px; margin: 20px 0; display: inline-block; border: 2px dashed #042a44; padding: 10px 20px; border-radius: 10px; color: #1CA3FD;">{otp}</div>
                        <a href="{reset_verification}" style="text-decoration: none; background: #1CA3FD; color: #FFFFFF; padding: 10px 20px; border-radius: 6px; display: inline-block; margin-top: 15px; font-weight: bold;">Verify Your Account</a>
                        <p style="text-align: center; margin-top: 20px;">If you did not request this, please ignore this email.</p>
                        <p style="text-align: center; margin-top: 20px;">For support, visit <a href="https://collegeinfonp.com/" style="text-decoration: none; color: #1CA3FD; font-weight: 600;">https://collegeinfonp.com/</a></p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span> +977 01-5244366</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Phone:</span> +977 9802348565 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> support@collegeinfonp.com</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""
    
    else:  # Password Reset Email
        body = f"""<body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="https://collegeinfoapi.vrittechnologies.com/media/gallery/images/College_Info_Nepal.png" alt="College Info Nepal Logo" width="150" style="display: block; margin: 0 auto;">
                        <p style="color: #1CA3FD; font-weight: 600; font-size: 18px; margin-top: 20px;">College Info Nepal</p>
                        <p style="color: #1CA3FD; font-weight: 600; font-size: 18px; margin-top: 20px;">Reset Your Password</p>
                        <p style="text-align: center; font-weight: 400;">Your OTP code to reset your password is:</p>
                        <div style="font-size: 32px; font-weight: bold; letter-spacing: 15px; margin: 20px 0; display: inline-block; border: 2px dashed #042a44; padding: 10px 20px; border-radius: 10px; color: #1CA3FD;">{otp}</div>
                        <p style="text-align: center; margin-top: 20px;">If you did not request this, please ignore this email.</p>
                        <p style="text-align: center; margin-top: 20px;">For support, visit <a href="https://collegeinfonp.com/" style="text-decoration: none; color: #1CA3FD; font-weight: 600;">https://collegeinfonp.com/</a></p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span> +977 01-5244366</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Phone:</span> +977 9802348565 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> support@collegeinfonp.com</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""

    html_contents = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{'Verify Your Account' if reset_verification == 'verification' else 'Reset Your Password'}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                    color: #1CA3FD;
                }}
            </style>
        </head>
        {body}
        </html>"""

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, "", email_from, recipient_list, html_message=html_contents)



class ContactmeView(generics.GenericAPIView):    
    serializer_class = ContactMeSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]
        subject = serializer.data.get('subject')
        full_name = serializer.data["full_name"]
        message = serializer.data["message"]
        phone = serializer.data.get("phone")
        
        ContactMe(email,full_name,phone,subject,message)
           
        return response.Response(
            {
            "message": "Email has sent to College Info Nepal Owner, please kindly wait for response"
            },
            status=status.HTTP_200_OK,
        )
     
# class SendEmailForBookingVerification(APIView):
#     serializer_class = EmailNumberSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             try:
#                 book = DestinationBook.objects.get(email=email)
#             except DestinationBook.DoesNotExist:
#                 return Response({'detail': 'Booking details with this email do not exist.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Construct the verification URL
#             site_url = 'https://example.com'  
#             verify_url = f"{site_url}/user-verification-success?pk={urlsafe_base64_encode(force_bytes(book.pk))}"

#             # Fetch the admin email from the User model
#             admin_user = CustomUser.objects.filter(is_superuser=True).first()
#             if admin_user:
#                 admin_name = admin_user.first_name
#                 admin_email = admin_user.email
#             else:
#                 return Response({'detail': 'Admin email not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Send the confirmation email
#             subject = 'Booking Verification Email'
#             send_booking_confirmation_email(email, verify_url, subject, book, admin_email, admin_name)

#             return Response({'detail': 'Email for Booking confirmation sent successfully'}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def send_booking_confirmation_email(email, verify_url, subject, book, admin_email, admin_name):
#     context = {
#         'admin_name': admin_name,
#         'recipient_name': book.full_name,
#         'contact': book.phone_number,
#         'destination': book.destination.destination_title,
#         'arrival_date': book.arrival_date.strftime('%d/%m/%Y'),
#         'departure_date': book.departure_date.strftime('%d/%m/%Y'),
#         'preferred_service_type': book.service_type,
#     }

#     # Conditionally add 'activity' if it's not None
#     if book.activity:
#                 context['activity'] = book.activity.name

#                 # Conditionally add 'package' if it's not None
#     if book.package:
#                 context['package'] = book.package.name


#     html_content = render_to_string('booking_confirmation.html', context)
#     from_email = f'Everest Thrills <{admin_email}>'

#     # Send email to the customer
#     recipient_list = [email]
#     send_mail(subject, '', from_email, recipient_list, html_message=html_content)

#     # Send email to the admin
#     admin_subject = f"New Trip Booking Notification - {book.full_name}"
#     admin_context = context.copy()
#     admin_context['verification_url'] = verify_url
#     admin_html_content = render_to_string('admin_booking_notification.html', admin_context)

#     admin_recipient_list = [admin_email]
#     send_mail(admin_subject, '', from_email, admin_recipient_list, html_message=admin_html_content)


class PasswordResetView(generics.GenericAPIView):

            def generate_otp(self,user):
                # Generate a random 5-digit OTP
                # return "12345"
                user = str(user)
                return user[0]+''.join(random.choices(string.digits, k=4)) + user[-1]
            
            serializer_class = PasswordNumberSerializer
            def post(self, request):
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                email = serializer.data["email"]
                user = CustomUser.objects.filter(Q(email=email) | Q(phone = email)).first()
                if user:
                
                    otp = self.generate_otp(user.id)

                    email_type = "reset_password"
                    
                    subject = 'Everest Thrill Password Reset OTP'
                    if '@' in email:
                        email = user.email
                        sendPasswordResetMail(email, otp,subject,email_type,user)
                    else:
                        SendSms(contact=email,otp=otp,message=subject)
                
                    cache_key = f"password_reset_otp_{user.id}"
                    cache.set(cache_key, otp, timeout=otp_time_expired)

                    return response.Response(
                        {
                        "message":"OTP has been sent to your email address"
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return response.Response(
                        {"message": "User doesn't exists"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

def sendPasswordResetMail(email, otp, subject, email_type, user):
    password_html_contents = ""  # Initialize to avoid UnboundLocalError
            
    if email_type == "reset_password":  # Ensure this matches what is passed
                context = {
                    'otp': otp,
                    'user': user,
                    'verification_url': 'https://example.com/verify'
                }
                
                password_html_contents = render_to_string('reset_password_otp.html', context)
            
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    plain_message = ""
    send_mail(subject, plain_message, email_from, recipient_list, html_message=password_html_contents)
    


class CustomChangePasswordView(generics.GenericAPIView):
    serializer_class = CustomChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)

        # Retrieve user based on email or phone
        user = CustomUser.objects.filter(
            Q(email=serializer.validated_data.get('email')) |
            Q(phone=serializer.validated_data.get('email'))
        ).first()

        if not user:
            return response.Response(
                {"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verify old password
        old_password = serializer.validated_data.get('old_password')
        if not check_password(old_password, user.password):
            return response.Response(
                {"message": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if new password matches re-entered password
        new_password = serializer.validated_data.get('new_password')
        confirm_new_password = serializer.validated_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            return response.Response(
                {"message": "New passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set and save new password
        user.set_password(new_password)  # Hashes the password securely
        user.save()

        return response.Response(
            {"message": "Password successfully changed"},
            status=status.HTTP_200_OK
        )
