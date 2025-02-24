from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import College
from ..serializers.college_serializers import CollegeListSerializers, CollegeRetrieveSerializers, CollegeWriteSerializers, CollegeAdminWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from mainproj.permissions import DynamicModelPermission
from ..utilities.filter import CollegeFilter
from ..utilities.pagination import MyPageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Field
from accounts.models import CustomUser as User


class collegeViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeListSerializers
    # permission_classes = [collegemanagementPermission]
    # permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    lookup_field = "slug"
    queryset = College.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','slug','name', 'established_date', 'website_link', 'address', 'phone_number', 'email','google_map_link', 'latitude', 'longitude', 'about', 'brochure', 'created_date', 'updated_date']
    ordering_fields = ['id','slug','name', 'established_date', 'website_link', 'address', 'district__name', 'phone_number', 'email', 'latitude', 'longitude', 'about', 'brochure', 'step_counter', 'placement', 'scholarship', 'created_date', 'updated_date']
    filterset_class= CollegeFilter
    # ('name', 'established_date', 'website_link', 'address', 'district', 'phone_number', 'email', 'affiliated', 'college_type', 'discipline', 'social_media', 'google_map_link', 'latitude', 'longitude', 'about', 'brochure', 'step_counter', 'facilities', 'placement', 'scholarship', 'created_date', 'updated_date', )

    # filterset_fields = {
    #     'id': ['exact'],
    #     'college_type': ['exact'],
    #     'affiliated': ['exact'],
    #     'established_date': ['exact','gte','lte'],
    #     'created_date': ['exact','gte','lte'],
    #     'updated_date': ['exact','gte','lte'],
    # }

    def get_queryset(self):
        # print(self.action)
        queryset = super().get_queryset()
        request = self.request
        if request.user.is_superuser:
            return queryset
        elif request.user.has_perm('collegemanagement.change_college'):
            return queryset.filter(user=request.user)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeWriteSerializers
        elif self.action == 'retrieve':
            return CollegeRetrieveSerializers
        elif self.action in ['college_creation']:
            return CollegeAdminWriteSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path="college-logo")
    def get_dp_image(self, request, pk=None):
        colleges = College.objects.all()  # Fetch all colleges
        if not colleges.exists():
            return Response({"error": "No colleges available."}, status=404)

        logos = []
        for college in colleges:
            if college.dp_image:
                dp_image_url = request.build_absolute_uri(college.dp_image.url)
                logos.append({"slug": college.slug, "college_name": college.name, "dp_image_url": dp_image_url})

        if not logos:
            return Response({"message": "No display images available."}, status=404)

        return Response(logos, status=200)
    
    @action(detail=False, methods=['post'], name="college_creation", url_path="college-creation")
    def college_creation(self, request, *args, **kwargs):
        """
        Authenticate user from access token in payload if not in headers.
        Ensure the user has permission to add a college.
        """
        # If the user is not already authenticated via headers, check token in payload
        if not request.user.is_authenticated:
            access_token = request.data.get("accessToken")

            if not access_token:
                return Response(
                    {"error": "Authentication credentials were not provided! Access token required in payload."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Authenticate user using JWT
            jwt_authenticator = JWTAuthentication()
            try:
                validated_token = jwt_authenticator.get_validated_token(access_token)
                user = jwt_authenticator.get_user(validated_token)
            except Exception:
                return Response(
                    {"error": "Invalid or expired access token!"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Assign the authenticated user to request
            request.user = user

        # ✅ **Force Refresh User Permissions (Fixes Permission Cache Issue)**
        request.user = User.objects.get(id=request.user.id)

        # ✅ **Check if user has 'add_college' permission**
        if not request.user.has_perm("collegemanagement.add_college"):  
            return Response(
                {"error": "You do not have permission to add a college."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ **Now create the college since the user is authenticated and has permission**
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            college = serializer.save()  # Create the college instance
            
            # Assign the created college to the authenticated user
            request.user.college = college
            request.user.save()

            return Response(
                {"message": "College created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    @action(detail=False, methods=['get'], name="calculate_completion_percentage", url_path="completion-percentage")
    def calculate_completion_percentage(self, request, *args, **kwargs):
        """
        Calculate the profile completion percentage, but restrict access only to assigned college admins.
        """
        user = request.user

        # Check if user has a related college (assuming a OneToOne or ForeignKey relationship)
        if not hasattr(user, "college") or not user.college:
            return Response({"error": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)

        # Get the user's assigned college
        college = user.college

        # Identify required fields dynamically
        required_fields = [
            field.name for field in College._meta.get_fields()
            if isinstance(field, Field) and not field.blank and not field.null
        ]

        # Count filled fields
        completed_fields_count = sum(1 for field in required_fields if getattr(college, field, None))
        total_required_fields = len(required_fields)

        # Calculate completion percentage
        completion_percentage = (completed_fields_count / total_required_fields * 100) if total_required_fields else 100

        completion_data = {
            "college_id": college.id,
            "college_name": college.name,
            "completion_percentage": round(completion_percentage, 2),
        }

        return Response(completion_data)
