from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password,check_password

from django.core.cache import cache
from django.db.models import Q

def TokenValidate(token,email,key):
    user = CustomUser.objects.filter(Q(email=email))
    if user.exists():
        user = user.first()
        user_check_key = key+str(user.id)
        token_access = cache.get(user_check_key)
        if token_access == token:
            user.is_verified = True
            user.save()
            return True
    return False
    

class TokenValidationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.CharField()
    
    def validate_otp(self, value):
        # Perform your token validation logic here
        email = self.initial_data.get('email')  # Access email from initial data
        if not TokenValidate(value,email,"password_reset_otp_"):
            raise serializers.ValidationError("Invalid token")
        return value

        
class CustomPasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=4)
    email = serializers.CharField()

    class Meta:
        fields = '__all__'

    def validate_password(self, value):
        # Hash the password using Django's make_password function
        return make_password(value)
    
    def validate_token(self, value):
        # Perform your token validation logic here
        email = self.initial_data.get('email')  # Access email from initial data
        if not TokenValidate(value,email,"password_reset_otp_"):
            raise serializers.ValidationError("Invalid token")
        return value
    
    def validate(self, attrs):
        attrs  =  super().validate(attrs)
 
        if TokenValidate(self.initial_data.get('token') ,self.initial_data.get('email'),"password_reset_otp_"):
            attrs['token_validate'] = True
        else:
            attrs['token_validate'] = False
        return attrs
    
class EmailResetSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=5)
    second_email = serializers.EmailField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

    class Meta:
        fields = '__all__'


    def validate_token(self, value):
        print("validiting token")
        # Perform your token validation logic here
        email = self.initial_data.get('email')  # Access email from initial data
        
        if not TokenValidate(value,email,"email_reset_otp_"):
            raise serializers.ValidationError("Invalid token")
        return value
    

    def validate_email(self, value):

        email = self.initial_data.get('email')  # Access email from initial data
        

        user = CustomUser.objects.filter(Q(email=email))
        if not user.exists():
            raise serializers.ValidationError("Your account does not exists!.")
        return value
    
    def validate_password(self, value):

        email = self.initial_data.get('email')  # Access email from initial data
        input_password = self.initial_data.get('password')

        user = CustomUser.objects.filter(Q(email=email))
        if not user.exists():
            raise serializers.ValidationError("Your account does not exists | You are unauthorized user.")
        if not check_password(input_password,CustomUser.objects.get(email=email).password):
            raise serializers.ValidationError("You are unauthorized user")
     
        return value
     
    
    def validate(self, attrs):
        attrs  =  super().validate(attrs)

        if TokenValidate(self.initial_data.get('token') ,self.initial_data.get('email'),"email_reset_otp_"):
            attrs['token_validate'] = True
        else:
            attrs['token_validate'] = False
        return attrs

 
class EmailNumberSerializer(serializers.Serializer):
    email = serializers.EmailField()

class EmailChangeGetOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    second_email = serializers.EmailField()


class ContactMeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    subject = serializers.CharField(required = False)
    message = serializers.CharField()
    phone = serializers.CharField(required = False)
    full_name =  serializers.CharField()

# class EmailNumberSerializer(serializers.Serializer):
    # email = serializers.EmailField()
#     type = serializers.ChoiceField(choices=[
#         ('verification', 'Verification'),
#         ('reset_password', 'Reset Password')
#     ])
    
class PasswordNumberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # type = serializers.ChoiceField(choices=[
    #     ('verification', 'Verification'),
    #     ('reset_password', 'Reset Password')
    # ])

class CustomChangePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if len(data.get('new_password')) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return data
