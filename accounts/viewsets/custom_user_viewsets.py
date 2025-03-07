from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..serializers.custom_user_serializers import CustomUserReadSerializer, CustomUserWriteSerializer, CustomUserRetrieveSerializer,CustomUserChangePasswordSerializers,CustomUserWriteSerializersCollegeAdmin
from rest_framework.response import Response
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from ..utilities.pagination import MyPageNumberPagination
from accounts.utilities.filters import CustomUserFilter
# accounts/utilities/filters.py
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from mainproj.permissions import *
from mainproj.permissions import DynamicModelPermission
from rest_framework.permissions import IsAuthenticated,AllowAny

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    permission_classes = [DynamicModelPermission]
    filterset_class = CustomUserFilter
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    
    search_fields = ['position', 'email','first_name','last_name','groups__name']
    ordering_fields =['position', 'email','first_name','last_name','id','created_date','updated_date']


    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.is_staff:
            return super().get_queryset()
        elif self.request.user.is_authenticated:
            return super().get_queryset().filter(id=self.request.user.id)
        else:
            return CustomUser.objects.none()


    def get_serializer_class(self):
        if self.action in ['list']:
            return CustomUserReadSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CustomUserWriteSerializer
        elif self.action in ['signup_college_admin']:
            return CustomUserWriteSerializersCollegeAdmin
        elif self.action in ['retrieve']:
            return CustomUserRetrieveSerializer
        elif self.action in ['changePassword']:
            return CustomUserChangePasswordSerializers
        return CustomUserReadSerializer
    
    @action(detail=False, methods=['post'], name="changePassword", url_path="change-password",permission_classes=[IsAuthenticated])
    def changePassword(self, request, *args, **kwargs):
        serializer = CustomUserChangePasswordSerializers(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user  # Get the current authenticated user
            user.set_password(serializer.validated_data['new_password'])  # Hash and set the new password
            user.save()  # Save the updated user instance
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], name="GetSelfDetail", url_path="me",permission_classes=[IsAuthenticated])
    def GetSelfDetail(self, request, *args, **kwargs):
        self.object = request.user  # Set the object directly to the current user
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], name="college_admins", url_path="college-admins", permission_classes=[IsAuthenticated])
    def college_admins(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(college__isnull=False)  # Filter users with assigned college
        page = self.paginate_queryset(queryset)  # Apply pagination
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # Return paginated response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)  # If pagination is not applied, return normal response


    @action(detail=False, methods=['post'], name="signup_college_admin", url_path="signup-college-admin")
    def signup_college_admin(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  

        if serializer.is_valid():
            serializer.save()
            # Generate tokens for the newly created user
            user = serializer.instance
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response(
                {
                    "message": "College Admin signed up successfully!",
                    "data": serializer.data,
                    "access": access_token,
                    "refresh": refresh_token
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
