from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import RequestSubmission
from ..serializers.requestsubmission_serializers import RequestSubmissionListSerializers, RequestSubmissionRetrieveSerializers, RequestSubmissionWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission

class requestsubmissionViewsets(viewsets.ModelViewSet):
    serializer_class = RequestSubmissionListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = RequestSubmission.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','subject','description','user__username','user__first_name'] 
    ordering_fields =  ['id','subject','description']

    filterset_fields = {
        'id': ['exact'],
        'user': ['exact'],
        'subject': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RequestSubmissionWriteSerializers
        elif self.action == 'retrieve':
            return RequestSubmissionRetrieveSerializers
        return super().get_serializer_class()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})  # Pass request to serializer
        return context

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

