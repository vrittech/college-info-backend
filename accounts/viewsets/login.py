from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..serializers.custom_user_serializers import CustomUserReadSerializer
from rest_framework.response import Response
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        ),
        # responses={200: MyResponseSerializer},
        operation_summary="Login and get token",
        operation_description="Login and get token",
    )
    @csrf_exempt
    def post(self, request):
        username_or_email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using either username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            user = authenticate(request, email=username_or_email, password=password)

        # If the user is authenticated, log them in and generate tokens
        if user is not None:
            if user.is_active == False:
                return Response({'error': 'Your Account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_obj = CustomUserReadSerializer(request.user,context={'request': request}) 
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_obj.data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # If the user is not authenticated, return an error message
        else:
            from django.db.models import Q
            user_obj = CustomUser.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
            if user_obj.exists():
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid username/email'}, status=status.HTTP_401_UNAUTHORIZED)

