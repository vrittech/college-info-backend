from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import EmailSetup
from ..serializers.emailsetup_serializers import EmailSetupListSerializers, EmailSetupRetrieveSerializers, EmailSetupWriteSerializers
from ..utilities.importbase import *

class emailsetupViewsets(viewsets.ModelViewSet):
    serializer_class = EmailSetupListSerializers
    # permission_classes = [setupemailPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = EmailSetup.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmailSetupWriteSerializers
        elif self.action == 'retrieve':
            return EmailSetupRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

