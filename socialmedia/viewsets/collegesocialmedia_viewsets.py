from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeSocialMedia
from ..serializers.collegesocialmedia_serializers import CollegeSocialMediaListSerializers, CollegeSocialMediaRetrieveSerializers, CollegeSocialMediaWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission
from rest_framework.response import Response
from rest_framework import status

class collegesocialmediaViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeSocialMediaListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeSocialMedia.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name__name']
    ordering_fields = ['id','name']

    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
        'college': ['exact'],
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
            return CollegeSocialMediaWriteSerializers
        elif self.action == 'retrieve':
            return CollegeSocialMediaRetrieveSerializers
        return super().get_serializer_class()
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        college_social_media = serializer.save()
        
        # Return the serialized object using CollegeSocialMediaRetrieveSerializers
        response_serializer = CollegeSocialMediaRetrieveSerializers(college_social_media)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

