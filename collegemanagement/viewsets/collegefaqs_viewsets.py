from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeFaqs
from ..serializers.collegefaqs_serializers import CollegeFaqsListSerializers, CollegeFaqsRetrieveSerializers, CollegeFaqsWriteSerializers
from ..utilities.importbase import *
from mainproj.permissions import DynamicModelPermission
from ..utilities.pagination import MyPageNumberPagination

class collegefaqsViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeFaqsListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeFaqs.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        if self.request.user.college:
            return super().get_queryset().filter(college = self.request.user.college)
        
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeFaqsWriteSerializers
        elif self.action == 'retrieve':
            return CollegeFaqsRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

