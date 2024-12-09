from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from advertisement.models import Advertisement
from affiliation.models import Affiliation
from certification.models import Certification
from informationmanagement.models import Information
from collegemanagement.models import College, CollegeGallery, CollegeFaqs, CollegeType
from collegetype.models import CollegeType
from contact.models import Contact
from coursemanagement.models import Course
from district.models import District
from facilities.models import Facility
from faculty.models import Faculty
from level.models import Level
from socialmedia.models import SocialMedia
from superadmindetails.models import SuperAdminDetails         

VALID_TYPES = {
    "advertisement": Advertisement,
    "affiliation": Affiliation,
    "certification": Certification,
    "information": Information,
    "college": College,
    "college-gallery": CollegeGallery,
    "college-faqs": CollegeFaqs,
    "college-type": CollegeType,
    "contact": Contact,
    "course": Course,
    "district": District,
    "facility": Facility,
    "faculty": Faculty,
    "level": Level,
    "social-media": SocialMedia,
    "super-admin-details": SuperAdminDetails,
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
        # Extract 'delete_ids' and 'type' from request data
        delete_ids = request.data.get('delete_ids')
        delete_type = request.data.get('type')

        # Validate input: Check for missing or invalid input
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

        # Get the model based on delete_type
        model = VALID_TYPES[delete_type]
        
        # Fetch the queryset based on the provided IDs
        queryset = model.objects.filter(id__in=delete_ids)

        # Check if any of the delete_ids do not exist
        existing_ids = list(queryset.values_list('id', flat=True))
        missing_ids = set(delete_ids) - set(existing_ids)

        if missing_ids:
            return Response(
                {"error": f"IDs not found: {list(missing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform the bulk deletion
        deleted_count, _ = queryset.delete()

        return Response(
            {"message": f"Successfully deleted {deleted_count} items of type '{delete_type}'."},
            status=status.HTTP_200_OK
        )
