from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CoursesAndFees
from coursemanagement.models import Course
from ..serializers.coursesandfees_serializers import CoursesAndFeesListSerializers, CoursesAndFeesRetrieveSerializers, CoursesAndFeesWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from mainproj.permissions import DynamicModelPermission
from django.shortcuts import get_object_or_404


class coursesandfeesViewsets(viewsets.ModelViewSet):
    serializer_class = CoursesAndFeesListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CoursesAndFees.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'is_admission': ['exact'],
        'college__slug': ['exact'],
        'course__slug': ['exact'],
    }

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = super().get_queryset().filter(college = self.request.user.college)
        else:
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
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path="average-course-fee/(?P<slug>[^/.]+)")
    def average_course_fee(self, request, slug=None, *args, **kwargs):
        """
        Fetch the average fee for a given course using its slug.
        """
        # Fetch the course using the slug
        course = get_object_or_404(Course, slug=slug)

        # Calculate the overall average fee for the given course
        average_fee = (
            CoursesAndFees.objects.filter(course=course, amount__isnull=False)
            .aggregate(overall_average_fee=Avg('amount'))
        )

        # Check if data exists
        if average_fee['overall_average_fee'] is None:
            return Response({"message": "No fee data available for the specified course."}, status=404)

        return Response({
            "course_slug": slug,
            "course_name": course.name,  # Assuming `name` field exists
            "overall_average_fee": average_fee['overall_average_fee']
        }, status=200)
