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
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


class collegeViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeListSerializers
    # permission_classes = [collegemanagementPermission]
    permission_classes = [DynamicModelPermission]
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

    # def get_lookup_field(self):
    #     return super.get_lookup_field()
    
    def get_object(self):
        """
        Override get_object to allow lookup by either 'id' or 'slug'.
        """
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)  # Get lookup value from URL
        if lookup_value.isdigit():  # Check if lookup_value is numeric (ID)
            return get_object_or_404(queryset, id=int(lookup_value))
        return get_object_or_404(queryset, slug=lookup_value)  # Otherwise, lookup by slug

    
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
    
    @action(detail=False, methods=['get'], url_path="college-logo", permission_classes=[AllowAny])
    def get_dp_image(self, request, pk=None):
        # Filter out colleges that have a dp_image before paginating
        colleges = College.objects.exclude(dp_image__isnull=True).exclude(dp_image="")  

        if not colleges.exists():
            return Response({"error": "No colleges with display images available."}, status=404)

        # Use your custom pagination class
        paginator = MyPageNumberPagination()
        paginated_colleges = paginator.paginate_queryset(colleges, request, view=self)

        # Construct response
        logos = [
            {"slug": college.slug, "college_name": college.name, "dp_image_url": request.build_absolute_uri(college.dp_image.url)}
            for college in paginated_colleges
        ]

        return paginator.get_paginated_response(logos)
    
    @action(
        detail=False,
        methods=['post'],
        name="college_creation",
        url_path="college-creation",
        permission_classes=[collegemanagementPermission] 
    )
    def college_creation(self, request, *args, **kwargs):
        # print(request.data.get("accessToken"),"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        """
        Authenticate user from access token in payload if not in headers.
        Ensure the user is either in the "College Admin" group or has the
        'collegemanagement.add_college' permission.
        """
        # If the user is not already authenticated via headers, check token in payload.
        if not request.user.is_authenticated:
            access_token = request.data.get("accessToken")
            if not access_token:
                return Response(
                    {"error": "Authentication credentials were not provided! Access token required in payload."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            jwt_authenticator = JWTAuthentication()
            try:
                validated_token = jwt_authenticator.get_validated_token(access_token)
                user = jwt_authenticator.get_user(validated_token)
            except Exception:
                return Response(
                    {"error": "Invalid or expired access token!"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            # Assign the authenticated user to the request.
            request.user = user

        # Force-refresh user instance to update permissions (fix permission cache issues).
        request.user = User.objects.get(id=request.user.id)

        # Manual check: Allow the action if the user is in the "College Admin" group
        # or if they have the "collegemanagement.add_college" permission.
        if not (request.user.groups.filter(name="College Admin").exists() or 
                request.user.has_perm("collegemanagement.add_college")):
            return Response(
                {"error": "You do not have permission to add a college."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Proceed to create the college.
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            college = serializer.save()  # Create the college instance.
            
            # Optionally assign the created college to the authenticated user.
            request.user.college = college
            request.user.save()

            return Response(
                {"message": "College created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], name="calculate_completion_percentage", url_path="completion-percentage/(?P<slug>[^/.]+)", permission_classes=[AllowAny])
    def calculate_completion_percentage(self, request, slug=None, *args, **kwargs):
        """
        Calculate the profile completion percentage for a specific college by slug.
        This API does NOT return completion percentage unless a slug is provided.
        """
        if not slug:
            return Response({"error": "A college slug is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the college using slug
        college = College.objects.filter(slug=slug).first()
        if not college:
            return Response({"error": "College not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the college data
        college_data = CollegeRetrieveSerializers(college).data

        ### 🔹 REQUIRED FIELDS (Must be filled)
        required_fields = [
            field.name for field in College._meta.get_fields()
            if hasattr(field, 'blank') and not field.blank and hasattr(field, 'null') and not field.null
        ]

        completed_required_fields = sum(1 for field in required_fields if getattr(college, field, None))
        total_required_fields = len(required_fields)

        ### 🔹 NON-REQUIRED FIELDS (Optional but contribute)
        non_required_fields = [
            field.name for field in College._meta.get_fields()
            if hasattr(field, 'blank') and field.blank and hasattr(field, 'null') and field.null
        ]

        completed_non_required_fields = sum(1 for field in non_required_fields if getattr(college, field, None))
        total_non_required_fields = len(non_required_fields)

        ### 🔹 RELATED FIELDS (Many-to-Many or ForeignKey relationships)
        related_fields = ["district", "affiliated", "college_type", "discipline", "social_media", "facilities"]
        completed_related_fields = sum(1 for field in related_fields if college_data.get(field))
        total_related_fields = len(related_fields)

        ### ✅ WEIGHTED COMPLETION CALCULATION:
        required_percentage = (completed_required_fields / total_required_fields * 60) if total_required_fields else 60
        related_percentage = (completed_related_fields / total_related_fields * 30) if total_related_fields else 30
        non_required_percentage = (completed_non_required_fields / total_non_required_fields * 10) if total_non_required_fields else 10

        completion_percentage = required_percentage + related_percentage + non_required_percentage

        completion_data = {
            "college_id": college.id,
            "slug": college.slug,
            "college_name": college.name,
            "completion_percentage": round(completion_percentage, 2)
        }

        return Response(completion_data, status=200)
