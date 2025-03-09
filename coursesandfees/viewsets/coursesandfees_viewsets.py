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
from rest_framework.response import Response
from rest_framework import status
from collegemanagement.models import College
from django.db.models import Avg, Count, Q


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
        'course__affiliation__id': ['exact'],  # Filter by affiliation
    }

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         queryset = super().get_queryset().filter(college = self.request.user.college)
    #     else:
    #         queryset = super().get_queryset()
    #     return queryset

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
            return CoursesAndFeesWriteSerializers
        elif self.action == 'retrieve':
            return CoursesAndFeesRetrieveSerializers
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        """ Override create method to return retrieve response format """
        write_serializer = CoursesAndFeesWriteSerializers(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()

        # After saving, use the retrieve serializer
        retrieve_serializer = CoursesAndFeesRetrieveSerializers(instance)

        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, *args, **kwargs):
        """ Override destroy method to return 200 OK even if object does not exist """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
        except CoursesAndFees.DoesNotExist:
            return Response({"detail": "No CoursesAndFees found"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path="average-course-fee(?:/(?P<slug>[^/.]+))?")
    def average_course_fee(self, request, slug=None, *args, **kwargs):
        """
        Fetch the average fee for courses with filtering.
        - If a course slug is provided, return its average fee.
        - If no slug is provided, return the average fee for all courses.
        - Filter by affiliation, college, or other parameters.
        - Include duration.
        - Courses with no fee data should return `null` as their fee.
        """

        # Get optional filters from query parameters
        affiliation_id = request.query_params.get("affiliation", None)
        college_slug = request.query_params.get("college", None)

        if slug:
            # Fetch course by slug with optional affiliation filter
            course_query = Course.objects.filter(slug=slug).select_related("affiliation", "duration")
            if affiliation_id:
                course_query = course_query.filter(affiliation__id=affiliation_id)

            # Check if course exists after filtering
            course = get_object_or_404(course_query)

            # Calculate the average fee for the given course
            average_fee = (
                CoursesAndFees.objects.filter(course=course)
                .aggregate(overall_average_fee=Avg('amount'))
            )

            return Response({
                "course_slug": slug,
                "course_name": course.name,
                "affiliation_id": course.affiliation.id if course.affiliation else None,
                "affiliation_slug": course.affiliation.slug if course.affiliation else None,
                "affiliation_name": course.affiliation.name if course.affiliation else None,
                "duration_id": course.duration.id if course.duration else None,
                "duration_name": course.duration.name if course.duration else None,  # Assuming `name` exists in Duration
                "overall_average_fee": average_fee['overall_average_fee'],  # Will be `None` if no fees exist
            }, status=200)

        else:
            # Fetch all courses and apply filters
            courses_query = Course.objects.select_related("affiliation", "duration")
            if affiliation_id:
                courses_query = courses_query.filter(affiliation__id=affiliation_id)
            if college_slug:
                courses_query = courses_query.filter(courses_and_fees__college__slug=college_slug)

            # Fetch course details
            courses = courses_query.values(
                'name', 'slug',
                'affiliation__id', 'affiliation__slug', 'affiliation__name',
                'duration__id', 'duration__name'
            )

            # Build a dictionary of courses
            course_fees = {
                course['slug']: {
                    "course_name": course['name'],
                    "course_slug": course['slug'],
                    "affiliation_id": course['affiliation__id'],
                    "affiliation_slug": course['affiliation__slug'],
                    "affiliation_name": course['affiliation__name'],
                    "duration_id": course['duration__id'],
                    "duration_name": course['duration__name'],
                    "overall_average_fee": None,  # Default to null
                }
                for course in courses
            }

            # Fetch courses that have fee data
            fees = (
                CoursesAndFees.objects.filter(course__slug__in=course_fees.keys())
                .values('course__slug')
                .annotate(overall_average_fee=Avg('amount'))
            )

            # Update the dictionary with available fee data
            for fee in fees:
                course_fees[fee['course__slug']]["overall_average_fee"] = fee["overall_average_fee"]

            # Convert dictionary to list
            course_list = list(course_fees.values())

            # Paginate the response
            paginator = MyPageNumberPagination()
            paginated_courses = paginator.paginate_queryset(course_list, request)

            return paginator.get_paginated_response({"courses": paginated_courses})