from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CoursesAndFees
from ..serializers.coursesandfees_serializers import CoursesAndFeesListSerializers, CoursesAndFeesRetrieveSerializers, CoursesAndFeesWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

class coursesandfeesViewsets(viewsets.ModelViewSet):
    serializer_class = CoursesAndFeesListSerializers
    # permission_classes = [coursesandfeesPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = CoursesAndFees.objects.all().order_by('-id')

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
            return CoursesAndFeesWriteSerializers
        elif self.action == 'retrieve':
            return CoursesAndFeesRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path="average-course-fee")
    def average_course_fee(self, request, *args, **kwargs):
        course_id = request.query_params.get('course_id', None)
        if not course_id:
            return Response({"error": "course_id parameter is required."}, status=400)
        
        # Calculate the overall average fee for the given course
        average_fee = (
            CoursesAndFees.objects.filter(course_id=course_id, amount__isnull=False)
            .aggregate(overall_average_fee=Avg('amount'))
        )

        # Check if there is any data
        if average_fee['overall_average_fee'] is None:
            return Response({"message": "No fee data available for the specified course."}, status=404)
        
        return Response({"course_id": course_id, "overall_average_fee": average_fee['overall_average_fee']}, status=200)