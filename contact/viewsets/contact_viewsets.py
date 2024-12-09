from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Contact
from ..serializers.contact_serializers import ContactListSerializers, ContactRetrieveSerializers, ContactWriteSerializers
from ..utilities.importbase import *

class contactViewsets(viewsets.ModelViewSet):
    serializer_class = ContactListSerializers
    # permission_classes = [contactPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Contact.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'email', 'phone_number',]
    ordering_fields = ['id','name', 'email', 'phone_number',]
# ('name', 'email', 'phone_number', )
    filterset_fields = {
        'id': ['exact'],
        'tag': ['exact'],
        'created_date': ['exact','gte','lte'],
        'updated_date': ['exact','gte','lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContactWriteSerializers
        elif self.action == 'retrieve':
            return ContactRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

