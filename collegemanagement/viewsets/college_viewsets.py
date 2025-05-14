from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import College,CollegeGallery
from ..serializers.college_serializers import CollegeListSerializers, CollegeRetrieveSerializers, CollegeWriteSerializers, CollegeAdminWriteSerializers,CollegeListUserSerializers
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
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Case, When, IntegerField, Max

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

cache_time = 1800  # 15 minutes



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

    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     request = self.request
    #     user = request.user

        
    #     # Apply visibility filter for non-admin users in list/retrieve actions
    #     if self.action in ['list', 'retrieve'] and not request.user.is_superuser:
    #         queryset = queryset.filter(is_show=True)
        
    #     # Apply permission-based filtering
    #     if user.is_superuser or user.has_perm('collegemanagement.manage_college'):
    #         return queryset
    #     elif request.user.has_perm('collegemanagement.change_college'):
    #         return queryset.filter(user=request.user)
        
    #     return queryset.filter(is_show=True)  # Default case for unprivileged users
    
    def get_queryset(self):
        # Start with base querys
        queryset = College.objects.all()
        request = self.request
        user = request.user
        
        # Apply visibility filter for non-admin users in list/retrieve actions
        if self.action in ['list', 'retrieve'] and not user.is_superuser:
            queryset = queryset.filter(is_show=True)
        
        # Apply permission-based filtering
        if user.is_superuser or user.has_perm('collegemanagement.manage_college'):
            pass  # No additional filtering for superusers/managers
        elif user.has_perm('collegemanagement.change_college'):
            queryset = queryset.filter(user=user)
        else:
            queryset = queryset.filter(is_show=True)  # Default case for unprivileged users
        
        # Get the highest priority in the database
        max_priority = queryset.aggregate(Max('priority'))['priority__max'] or 0

        # Custom ordering - first by priority, then by verified status, and lastly by created_date
        if self.action == 'list':
            queryset = queryset.annotate(
                priority_null=Case(
                    When(priority__isnull=True, then=max_priority + 1),  # Assign a priority that is higher than any existing priority
                    default=0,  # Normal priorities will be 0
                    output_field=IntegerField()
                )
            ).order_by(
                'priority_null',      # First, NULL priorities come after non-NULL ones
                'priority',           # Then, colleges with the lowest priority first (highest priority)
                '-is_verified',       # Then, sort by verification status (verified first)
                '-created_date'       # Finally, by the newest created date (latest first)
            )
            
        return queryset

    def get_serializer_class(self):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated and self.action == 'list':
            # If user is not authenticated, return the CollegeListUserSerializers
            return CollegeListUserSerializers

        # If the user is authenticated, proceed with your original logic
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeWriteSerializers
        elif self.action == 'retrieve':
            return  CollegeRetrieveSerializers
        elif self.action == 'college_creation':
            return CollegeAdminWriteSerializers
        
        # Default serializer class for other actions
        return super().get_serializer_class()
    
    # List action caching
    def _list(self, request, *args, **kwargs):
        """Actual list implementation"""
        print("List - uncached version")
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="CollegeList"))
    def _cached_list(self, request, *args, **kwargs):
        """Cached version of list"""
        return self._list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_list(request, *args, **kwargs)
        return self._list(request, *args, **kwargs)

    # Retrieve action caching
    def _retrieve(self, request, *args, **kwargs):
        """Actual retrieve implementation"""
        print("Retrieve - uncached version")
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="CollegeRetrieve"))
    def _cached_retrieve(self, request, *args, **kwargs):
        """Cached version of retrieve"""
        return self._retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_retrieve(request, *args, **kwargs)
        return self._retrieve(request, *args, **kwargs)

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
            {"slug": college.slug, "college_name": college.name, "dp_image_url": college.dp_image.url}
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
    
    @action(detail=False, methods=['get'], name="college-lists", url_path="college-lists", permission_classes=[AllowAny])
    def latest_college_images(self, request):
        """
        Fetch unique college data with full dataset ordering before pagination,
        ensuring results are ordered across all pages.
        Includes latest 3 images from CollegeGallery.
        """

        # **Get the base queryset without duplicates**
        colleges = self.get_queryset().distinct()  # ✅ Ensure no duplicate data

        # **Apply Filtering Once**
        filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
        for backend in filter_backends:
            colleges = backend().filter_queryset(request, colleges, self)

        # **Apply Ordering Before Pagination**
        ordering_field = request.GET.get("ordering", "-created_date")  # Default: latest first
        colleges = colleges.order_by(ordering_field).distinct()  # ✅ Prevent duplicate ordering

        # **Apply Pagination**
        paginator = MyPageNumberPagination()
        paginated_colleges = paginator.paginate_queryset(colleges, request, view=self)

        if paginated_colleges is None:  # If pagination fails, return all results
            paginated_colleges = colleges

        # **Construct Response Data Without Duplication**
        response_data = []
        seen_colleges = set()  # ✅ Use a set to track unique colleges

        for college in paginated_colleges:
            if college.id in seen_colleges:  # Avoid duplicate entries
                continue
            seen_colleges.add(college.id)

            latest_images = CollegeGallery.objects.filter(college=college).order_by('-created_date')[:3]
            images_array = [image.image.url for image in latest_images]

            response_data.append({
                "college": {
                    "id": college.id,
                    "slug": college.slug,
                    "name": college.name,
                    "district": college.district.name if college.district else None,
                    "dp_image": college.dp_image.url if college.dp_image else None,
                    "address": college.address,
                    "swiper_images": images_array
                }
            })

        return paginator.get_paginated_response(response_data) 
    

    @action(detail=False, methods=['get', 'patch'], url_path='update-priorities')
    def update_priorities(self, request, *args, **kwargs):
        if request.method == 'GET':
            # Handle GET request - fetching data
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            # PATCH method - Update a single college's priority
            update = request.data  # Expecting a single update object, not a list

            if not isinstance(update, dict):
                return Response(
                    {'error': 'Expected an object for college update'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate that the update contains both 'id' and 'priority'
            if 'id' not in update:
                return Response(
                    {'error': '"id" must be provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the priority value (allow blank or null)
            priority_value = update.get('priority', None)  # Defaults to None if not provided

            # If priority is blank, set it to None (i.e., clear priority)
            if priority_value == '':
                priority_value = None

            # If priority is not NULL, ensure it's unique
            if priority_value is not None:
                if College.objects.filter(priority=priority_value).exclude(id=update['id']).exists():
                    return Response(
                        {'error': f'Priority {priority_value} is already assigned to another college'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Get the college to be updated
            try:
                college = College.objects.get(id=update['id'])
            except College.DoesNotExist:
                return Response(
                    {'error': f'College with ID {update["id"]} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update the college's priority
            college.priority = priority_value  # Set it to None if blank or NULL
            college.save()  # Save the updated college

            # Return the updated college data
            result = {
                'id': college.id,
                'name': college.name,
                'slug': college.slug,
                'priority': college.priority
            }

            return Response(result, status=status.HTTP_200_OK)
        
        
    @action(detail=True, methods=['get'], permission_classes=[AllowAny], url_path="delete-files")
    def delete_files(self, request, college_slug=None, *args, **kwargs):
        field_name = request.query_params.get("field_name")
        
        # Valid fields for deletion
        valid_fields = ['og_image', 'dp_image', 'brochure']
        
        # Ensure field_name is valid
        if field_name not in valid_fields:
            return Response({"detail": "Invalid field name."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the college object
        college = self.get_object()

        # Check if the field exists and delete it
        if hasattr(college, field_name):
            setattr(college, field_name, None)
            college.save()
            return Response("Successfully Deleted", status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Field not found on the object."}, status=status.HTTP_400_BAD_REQUEST)

    #TODO Bulk updates of priorities
    # @action(detail=False, methods=['get', 'patch'], url_path='update-priorities')
    # def update_riorities(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #             queryset = self.filter_queryset(self.get_queryset())
    #             page = self.paginate_queryset(queryset)
    #             if page is not None:
    #                 serializer = self.get_serializer(page, many=True)
    #                 return self.get_paginated_response(serializer.data)
    #             serializer = self.get_serializer(queryset, many=True)
    #             return Response(serializer.data)
        
    #     elif request.method == 'PATCH':
    #         # PATCH method - Update priorities 
    #         updates = request.data
            
    #         if not isinstance(updates, list):
    #             return Response(
    #                 {'error': 'Expected a list of college updates'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #         # Validate all updates have IDs and priority
    #         for item in updates:
    #             if 'id' not in item or 'priority' not in item:
    #                 return Response(
    #                     {'error': 'Each item must contain both "id" and "priority"'},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )

    #         college_ids = [item['id'] for item in updates]
            
    #         # Get existing colleges (only those we need to update)
    #         colleges = College.objects.filter(id__in=college_ids)
    #         college_map = {college.id: college for college in colleges}

    #         # Check for invalid IDs
    #         invalid_ids = set(college_ids) - set(college_map.keys())
    #         if invalid_ids:
    #             return Response(
    #                 {'error': f'Invalid college IDs: {invalid_ids}'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #         # Apply updates
    #         updated_colleges = []
    #         for update in updates:
    #             college = college_map[update['id']]
    #             college.priority = update['priority']
    #             updated_colleges.append(college)

    #         # Bulk update only the priority field
    #         College.objects.bulk_update(updated_colleges, ['priority'])

    #         # Return the updated colleges
    #         result = [
    #             {
    #                 'id': college.id,
    #                 'name': college.name,
    #                 'slug': college.slug,
    #                 'priority': college.priority
    #             }
    #             for college in updated_colleges
    #         ]

    #         return Response(result, status=status.HTTP_200_OK)

