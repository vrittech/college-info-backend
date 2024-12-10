from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pandas as pd

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from discipline.models import Discipline
from faculty.models import Faculty
from collegetype.models import CollegeType
from level.models import Level
from district.models import District
from duration.models import Duration

from discipline.serializers.discipline_serializers import DisciplineWriteSerializers
from faculty.serializers.faculty_serializers import FacultyWriteSerializers
from collegetype.serializers.collegetype_serializers import CollegeTypeWriteSerializers
from level.serializers.level_serializers import LevelWriteSerializers
from district.serializers.district_serializers import DistrictWriteSerializers
from duration.serializers.duration_serializers import DurationWriteSerializers


class ImportExel(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'excel_file': openapi.Schema(type=openapi.TYPE_FILE),
            },
            required=['excel_file']
        ),
        operation_summary="Upload Excel or CSV file",
        operation_description="Upload an Excel or CSV file for data import",
    )
    def post(self, request, type, format=None):
        file = request.FILES.get('excel_file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Determine the file type based on extension
        file_name = file.name.lower()
        if file_name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return Response({"error": "Unsupported file format. Please upload a CSV or Excel file."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert the DataFrame to a list of dictionaries
        datas = df.to_dict(orient='records')

        # Process the DataFrame based on the 'type' parameter
        if type == "discipline":
            create_update(Discipline, DisciplineWriteSerializers, datas, 'name')
        elif type == "faculty":
            create_update(Faculty, FacultyWriteSerializers, datas, 'name')
        elif type == "college-type":
            create_update(CollegeType, CollegeTypeWriteSerializers, datas, 'type')
        elif type == "level":
            create_update(Level, LevelWriteSerializers, datas, 'level')
        elif type == "district":
            create_update(District, DistrictWriteSerializers, datas, 'name')
        elif type == "duration":
            create_update(Duration, DurationWriteSerializers, datas, 'duration')
        else:
            return Response({"message": 'Unknown file type'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)


def create_update(my_model, my_serializer, datas, unique_field_name):
    for record in datas:
        existing_data = my_model.objects.filter(**{unique_field_name: record[unique_field_name]})
        if existing_data.exists():
            existing_data = existing_data.first()
            serializer = my_serializer(existing_data, data=record)
            if serializer.is_valid():
                serializer.save()
        else:
            serializer = my_serializer(data=record)
            if serializer.is_valid():
                serializer.save()
