from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeFacility
from ..serializers.collegefacility_serializers import CollegeFacilityListSerializers, CollegeFacilityRetrieveSerializers, CollegeFacilityWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db import IntegrityError

class collegefacilityViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeFacilityListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeFacility.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'college': ['exact'],
        'facility': ['exact'],
        'created_date': ['exact','gte','lte'],
    }

    def get_queryset(self):
        """Admins see all data, normal users see only their college's data"""
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset  # Superusers get all records
            else:
                return queryset.filter(college=self.request.user.college)  # Normal users get their college data only

        return queryset  # If unauthenticated (unlikely due to permissions), return all


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeFacilityWriteSerializers
        elif self.action == 'retrieve':
            return CollegeFacilityRetrieveSerializers
        return super().get_serializer_class()
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print(request.data,"line")
        
    #     if serializer.is_valid():
    #         try:
    #             college_facility = serializer.save()
                
    #             # Serialize response with the retrieve serializer (nested objects)
    #             response_serializer = CollegeFacilityRetrieveSerializers(college_facility)

    #             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    #         except IntegrityError:
    #             return Response({"error": "Invalid data. College and Facility are required."}, status=status.HTTP_400_BAD_REQUEST)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

