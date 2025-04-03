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
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.exceptions import ValidationError

class superadmindetailsViewsets(viewsets.ModelViewSet):
        serializer_class = SuperAdminDetailsListSerializers
        permission_classes = [IsAdminUser]
        # authentication_classes = [JWTAuthentication]
        pagination_class = MyPageNumberPagination
        queryset = SuperAdminDetails.objects.all().order_by('-id')
        filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
        search_fields = ['id','name', 'email']
        ordering_fields = ['id','name']

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
            

        @action(detail=False, methods=['get', 'post', 'put'], name="manage-super-admin-details", url_path="manage-super-admin-details", permission_classes=[IsAdminUser])
        def manage_super_admin_details(self, request, *args, **kwargs):
            # Fetch the first SuperAdminDetails record
            superadmin = SuperAdminDetails.objects.first()

            # Handle GET request to retrieve the current super admin details
            if request.method == 'GET':
                if superadmin:
                    # Use the appropriate serializer for retrieving the superadmin details
                    serializer = SuperAdminDetailsRetrieveSerializers(superadmin, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                return Response({"message": "No SuperAdminDetails found."}, status=status.HTTP_200_OK)

            # Handle POST/PUT for create or update
            superadmin_data = request.data  # No need to handle files if there aren't any

            try:
                if superadmin:
                    # Use the appropriate serializer for updating the existing SuperAdminDetails record
                    serializer = SuperAdminDetailsWriteSerializers(superadmin, data=superadmin_data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({"message": "SuperAdminDetails updated successfully."}, status=status.HTTP_200_OK)
                else:
                    # Use the appropriate serializer for creating a new SuperAdminDetails record if none exists
                    serializer = SuperAdminDetailsWriteSerializers(data=superadmin_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response({"message": "SuperAdminDetails created successfully.", "super_admin_id": serializer.instance.id}, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
