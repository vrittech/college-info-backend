from ..models import EmailSetup
from ..serializers.email_setup_serializers import EmailSetupListSerializers,EmailSetupRetrieveSerializers,EmailSetupWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action

class EmailSetupViewset(viewsets.ModelViewSet):
    serializer_class = EmailSetupListSerializers
    permission_classes = [AdminViewSetsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = EmailSetup.objects.all().order_by('-id')

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'user':['exact'],
    # }
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return EmailSetupWriteSerializers
        elif self.action in ['retrieve']:
            return EmailSetupRetrieveSerializers
        return super().get_serializer_class()
    
    # @action(detail=False, methods=['get'], name="EmailSetups", url_path="job-seekers")
    # def EmailSetups(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    