from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers.group_serializers import GroupSerializer
from ..utilities.pagination import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id','name']
    filterset_fields = {
        'id': ['exact'],
        'name': ['exact'],
    }


