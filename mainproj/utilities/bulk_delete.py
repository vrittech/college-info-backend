from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from accounts.viewsets.group_viewsets import GroupViewSet 

from advertisement.models import Advertisement
from affiliation.models import Affiliation
from certification.models import Certification
from informationmanagement.models import Information,InformationCategory,InformationFiles,InformationGallery,InformationTagging
from collegemanagement.models import College, CollegeGallery, CollegeFaqs, CollegeType
from coursesandfees.models import CoursesAndFees
from collegetype.models import CollegeType
from contact.models import Contact
from coursemanagement.models import Course,CourseCurriculumFile
from district.models import District
from facilities.models import Facility,CollegeFacility
from faculty.models import Faculty
from level.models import Level,SubLevel
from socialmedia.models import SocialMedia
from superadmindetails.models import SuperAdminDetails
from accounts.models import Group
from event.models import Event,EventCategory,EventGallery,EventOrganizer
from inquiry.models import Inquiry 
from discipline.models import Discipline    
from gallery.models import Gallery,Album 
from duration.models import Duration

VALID_TYPES = {
    "advertisement": Advertisement,
    "affiliation": Affiliation,
    "courses-and-fees": CoursesAndFees,
    "certification": Certification,
    "information": Information,
    "information-category": InformationCategory,
    "information-files": InformationFiles,
    "information-gallery": InformationGallery,
    "information-tag": InformationTagging,
    "college": College,
    "college-gallery": CollegeGallery,
    "college-faqs": CollegeFaqs,
    "college-type": CollegeType,
    "contact": Contact,
    "course": Course,
    "course-curriculum-file": CourseCurriculumFile,
    "district": District,
    "facility": Facility,
    "college-facility": CollegeFacility,
    "faculty": Faculty,
    "college-level": Level,
    "sub-level": SubLevel,
    "social-media": SocialMedia,
    "super-admin-details": SuperAdminDetails,
    "event": Event,
    "event-category": EventCategory,
    "event-gallery": EventGallery,
    "event-organizer": EventOrganizer,
    "inquiry": Inquiry,
    "discipline": Discipline,
    "album": Album,
    # 'group': Group,
    "gallery": Gallery,
    "duration": Duration,
}

class BulkDelete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'delete_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='List of IDs to be deleted'
                ),
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type of model to delete from. Options: blog, project, project_service, career, clients, faqs, testimonial, case_study.'
                ),
            },
            required=['delete_ids', 'type'],
        ),
        operation_summary="Bulk Delete Records",
        operation_description="Deletes records in bulk based on the provided IDs and type.",
        responses={
            200: openapi.Response(description="Data successfully deleted in bulk"),
            400: openapi.Response(description="Invalid request parameters or unknown data type"),
        }
    )
    def post(self, request, *args, **kwargs):
        delete_ids = request.data.get('delete_ids')
        delete_type = request.data.get('type')

        if not delete_ids or not isinstance(delete_ids, list) or not all(isinstance(id, int) for id in delete_ids):
            return Response(
                {"error": "Invalid 'delete_ids'. Provide a list of integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not delete_type or delete_type not in VALID_TYPES:
            return Response(
                {"error": "Invalid or missing 'type'. Provide a valid type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        model = VALID_TYPES[delete_type]
        queryset = model.objects.filter(id__in=delete_ids)

        existing_ids = list(queryset.values_list('id', flat=True))
        missing_ids = set(delete_ids) - set(existing_ids)

        if missing_ids:
            return Response(
                {"error": f"IDs not found: {list(missing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        skipped_ids = []
        deletable_objects = []

        for instance in queryset:
            try:
                if isinstance(instance, Group):
                    GroupViewSet.perform_protection_check(instance)
                deletable_objects.append(instance)
            except PermissionDenied:
                skipped_ids.append(instance.id)

        if deletable_objects:
            model.objects.filter(id__in=[obj.id for obj in deletable_objects]).delete()

        deleted_count = len(deletable_objects)

        return Response({
            "message": f"Successfully deleted {deleted_count} items of type '{delete_type}'.",
            "skipped_ids": skipped_ids,
            "note": "Some items were skipped due to protection rules." if skipped_ids else None
        }, status=status.HTTP_200_OK)
