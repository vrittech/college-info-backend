from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Inquiry
from ..serializers.inquiry_serializers import InquiryListSerializers, InquiryRetrieveSerializers, InquiryWriteSerializers
from ..utilities.importbase import *
from ..utilities.filter import InquiryFilter

class inquiryViewsets(viewsets.ModelViewSet):
    serializer_class = InquiryListSerializers
    # permission_classes = [inquiryPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Inquiry.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = InquiryFilter
    search_fields = ['id', 'full_name', 'email', 'phone', 'courses__name', 'colleges__name']  # Searchable fields
    ordering_fields = ['id', 'full_name', 'created_at', 'updated_at']  # Orderable fields
    ordering = ['id']  # Default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InquiryWriteSerializers
        elif self.action == 'retrieve':
            return InquiryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

