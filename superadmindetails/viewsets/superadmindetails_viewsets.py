from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import SuperAdminDetails
from ..serializers.superadmindetails_serializers import SuperAdminDetailsListSerializers, SuperAdminDetailsRetrieveSerializers, SuperAdminDetailsWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class superadmindetailsViewsets(viewsets.ModelViewSet):
    serializer_class = SuperAdminDetailsListSerializers
    permission_classes = [superadmindetailsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = SuperAdminDetails.objects.all().order_by('-id')
# ('name', 'email', 'phone_number', 'location', 'social_media_links', 'created_at', 'updated_at', )
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'email', 'phone_number', 'location', 'social_media_links', 'created_at', 'updated_at']
    ordering_fields = ['id','name', 'phone_number', 'location', 'social_media_links', 'created_at', 'updated_at']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'location': ['exact'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SuperAdminDetailsWriteSerializers
        elif self.action == 'retrieve':
            return SuperAdminDetailsRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
        

    @action(detail=False, methods=['post'], name="create-update", url_path="create-super-admin-details")
    def create_update_about_us(self, request, *args, **kwargs):
        # Retrieve data from request
        description = request.data.get('description', None)
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)
        location = request.data.get('location', None)
        messenger_link = request.data.get('messenger_link', None)
        facebook_link = request.data.get('facebook_link', None)
        x_link = request.data.get('x_link', None)
        youtube_link = request.data.get('youtube_link', None)
        linkedin_link = request.data.get('linkedin_link', None)

        # Validate required fields
        if not description:
            return Response({"error": "Description is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if SuperAdminDetails exists
        superadmin = SuperAdminDetails.objects.all()

        if superadmin.exists():
            # Update the existing SuperAdminDetails entry
            superadmin = superadmin.first()
            superadmin.description = description
            superadmin.name = name if name else superadmin.name
            superadmin.email = email if email else superadmin.email
            superadmin.phone_number = phone_number if phone_number else superadmin.phone_number
            superadmin.location = location if location else superadmin.location
            superadmin.messenger_link = messenger_link if messenger_link else superadmin.messenger_link
            superadmin.facebook_link = facebook_link if facebook_link else superadmin.facebook_link
            superadmin.x_link = x_link if x_link else superadmin.x_link
            superadmin.youtube_link = youtube_link if youtube_link else superadmin.youtube_link
            superadmin.linkedin_link = linkedin_link if linkedin_link else superadmin.linkedin_link
            
            superadmin.save()
            return Response({"message": "SuperAdminDetails updated successfully."}, status=status.HTTP_200_OK)
        else:
            # Create a new SuperAdminDetails entry
            new_superadmin = SuperAdminDetails.objects.create(
                description=description,
                name=name,
                email=email,
                phone_number=phone_number,
                location=location,
                messenger_link=messenger_link,
                facebook_link=facebook_link,
                x_link=x_link,
                youtube_link=youtube_link,
                linkedin_link=linkedin_link
            )
            return Response({"message": "SuperAdminDetails created successfully.", "super_admin_id": new_superadmin.id}, status=status.HTTP_201_CREATED)
