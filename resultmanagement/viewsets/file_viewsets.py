from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import File
from ..serializers.file_serializers import FileListSerializers, FileRetrieveSerializers, FileWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from rest_framework import status
from mainproj.permissions import DynamicModelPermission
import pandas as pd
import numpy as np

class fileViewsets(viewsets.ModelViewSet):
    serializer_class = FileListSerializers
    permission_classes = [resultmanagementPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = File.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'is_active': ['exact'],
        'created_date': ['exact', 'gte', 'lte'],
        'updated_date': ['exact', 'gte', 'lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FileWriteSerializers
        elif self.action == 'retrieve':
            return FileRetrieveSerializers
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        """
        1) Save the uploaded file into the File model.
        2) Read the first row to extract column headers.
        3) Read a 3×3 preview.
        4) Return { file_id, available_columns, sample_first_3_rows }.
        """
        uploaded_file = request.FILES.get('file', None)

        # 1) Validate that a file was uploaded
        if uploaded_file is None:
            return Response(
                {"error": "No file was uploaded. Please attach a CSV or Excel file under key 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Determine file extension (lowercased)
        filename = uploaded_file.name.lower()
        if filename.endswith('.csv'):
            file_type = 'csv'
        elif filename.endswith(('.xlsx', '.xls')):
            file_type = 'excel'
        else:
            return Response(
                {"error": "Unsupported file format. Only .csv, .xls, or .xlsx are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3) Save the File instance
        file_obj = File.objects.create(
            file=uploaded_file,
            is_active=False  # or True, depending on your logic
        )

        # 4) Read the first row to get column names
        try:
            uploaded_file.seek(0)
            if file_type == 'csv':
                df_header = pd.read_csv(uploaded_file, nrows=1)
            else:
                df_header = pd.read_excel(uploaded_file, nrows=1)
        except Exception as e:
            # If parsing fails, delete the File record so no orphan is left
            file_obj.delete()
            return Response(
                {"error": f"Error parsing the uploaded file to extract columns: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        original_columns = [str(col) for col in df_header.columns]

        # 5) Read a 3×3 sample of the data
        try:
            uploaded_file.seek(0)
            if file_type == 'csv':
                df_sample = pd.read_csv(uploaded_file, nrows=3)
            else:
                df_sample = pd.read_excel(uploaded_file, nrows=3)
        except Exception as e:
            file_obj.delete()
            return Response(
                {"error": f"Error parsing the uploaded file to get sample rows: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle edge cases for NaN and infinity values
        df_sample.replace([np.nan, np.inf, -np.inf], None, inplace=True)

        sample_sliced = df_sample.iloc[:, :3]  # Select only the first three columns
        sample_preview = sample_sliced.iloc[:3, :3]  # Take a 3x3 sample
        preview_records = sample_preview.to_dict(orient='records')

        # 6) Return file_id + column headers + preview
        return Response(
            {
                "file_id": file_obj.pk,
                "message": "Please select which columns to import.",
                "available_columns": original_columns,
                "sample_first_3_rows": preview_records
            },
            status=status.HTTP_201_CREATED
        )

       


    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)