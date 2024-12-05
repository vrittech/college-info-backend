from django.urls import path
from .views import EmailCheckView, CustomPasswordResetView , VerifyUserPasswordToken,ContactmeView,EmailChangeGetOtpView,EmailResetView
from .views import PasswordResetView



urlpatterns = [
    path('get-otp/', EmailCheckView.as_view()),
    path('password-reset-get-otp/', PasswordResetView.as_view()),
    # path('send-booking-confirmation/', SendEmailForBookingVerification.as_view()),
    path('get-otp-email-change/', EmailChangeGetOtpView.as_view()),
    path('email-reset/', EmailResetView.as_view(), name="EmailResetView"),
    path('password-reset/', CustomPasswordResetView.as_view(), name="reset-password"),
    path('verify-token/', VerifyUserPasswordToken.as_view(), name="VerifyUserPasswordToken"),

    path('contact-me/',ContactmeView.as_view(),name="ContactmeView"),
]
 