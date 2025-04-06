from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
import ast
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile  
from ..models import Course, CourseCurriculumFile, Duration, Faculty, Level, Discipline, Affiliation

def str_to_list(data, value_to_convert):
    try:
        mutable_data = data.dict()  # Convert to dictionary if possible
    except AttributeError:
        mutable_data = data  # Already a dictionary

    value_to_convert_data = mutable_data.get(value_to_convert)

    # If it's already a list, return as is
    if isinstance(value_to_convert_data, list):
        return mutable_data

    # Handle binary or file data (leave as is)
    if isinstance(value_to_convert_data, bytes):
        return mutable_data

    # If it's an int, float, or bool, wrap it in a list
    if isinstance(value_to_convert_data, (int, float, bool)):
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

    # If it's None, convert to an empty list
    if value_to_convert_data is None:
        mutable_data[value_to_convert] = []
        return mutable_data

    # Handle comma-separated values (e.g., "4,5,")
    if isinstance(value_to_convert_data, str) and "," in value_to_convert_data:
        parsed_list = [
            item.strip() for item in value_to_convert_data.split(",") if item.strip().isdigit()
        ]  # ✅ Remove empty strings and ensure only digits

        # Convert to integers
        mutable_data[value_to_convert] = [int(item) for item in parsed_list]
        return mutable_data

    # If it's a string, try parsing it as a list
    try:
        parsed_value = ast.literal_eval(value_to_convert_data)

        # Ensure parsed result is a list
        if isinstance(parsed_value, list):
            mutable_data[value_to_convert] = parsed_value
        else:
            # Convert string (that is not a list) into a single-item list
            mutable_data[value_to_convert] = [value_to_convert_data]

        return mutable_data

    except (ValueError, SyntaxError):
        # If parsing fails, wrap it in a list instead
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

    
    

# Serializer for Duration model
class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = ['id', 'name']
        
class CourseCurriculumFileSerializer(serializers.ModelSerializer):
    """Serializer for handling multiple curriculum file uploads"""

    class Meta:
        model = CourseCurriculumFile
        fields = ["id", "curriculum_file_upload", "uploaded_at"]


# Serializer for Faculty model
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']  

# Serializer for Level model
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']  

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        ref_name = 'course'
        fields = ['id', 'name','slug','university_type']  

# Serializer for Discipline model
class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name'] 

class CourseListSerializers(serializers.ModelSerializer):
    # Nested serializers for related fields
    affiliation = AffiliationSerializer(read_only=True)
    duration = DurationSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    discipline = DisciplineSerializer(many=True,read_only=True)
    curriculum_file_upload = CourseCurriculumFileSerializer(many=True, read_only=True)
    

    class Meta:
        model = Course
        fields = '__all__'


class CourseRetrieveSerializers(serializers.ModelSerializer):
    # Nested serializers for related fields
    affiliation = AffiliationSerializer(read_only=True)
    duration = DurationSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    discipline = DisciplineSerializer(many=True,read_only=True)
    curriculum_file_upload = CourseCurriculumFileSerializer(many=True, read_only=True)
    
    

    class Meta:
        model = Course
        fields = '__all__'


class CourseWriteSerializers(serializers.ModelSerializer):
    # Accept IDs for ForeignKey and ManyToMany fields in the request (write-only)
    # affiliation = serializers.PrimaryKeyRelatedField(
    #     queryset=Affiliation.objects.all(), required=False, write_only=True
    # )
    # duration = serializers.PrimaryKeyRelatedField(
    #     queryset=Duration.objects.all(), required=True, write_only=True
    # )
    # faculty = serializers.PrimaryKeyRelatedField(
    #     queryset=Faculty.objects.all(), required=True, write_only=True
    # )
    # level = serializers.PrimaryKeyRelatedField(
    #     queryset=Level.objects.all(), required=True, write_only=True
    # )
    # discipline = serializers.PrimaryKeyRelatedField(
    #     queryset=Discipline.objects.all(), many=True, required=True, write_only=True
    # )

    # Read-only: Return full objects instead of just IDs in the response
    affiliation = AffiliationSerializer(read_only=True)
    duration = DurationSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    discipline = DisciplineSerializer(many=True, read_only=True)
    # Retrieve curriculum files related to the course in the response
    curriculum_file_upload = CourseCurriculumFileSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        
    def to_internal_value(self, data):
            """Convert certification input from string to list using str_to_list."""
            data = str_to_list(data, 'discipline')  # Convert string to list for certification
            return super().to_internal_value(data)

    def create(self, validated_data):
        """Handles creating a course with multiple curriculum file uploads"""
        request = self.context.get("request")

        # Extract required foreign key fields from request.data instead of validated_data
        duration_id = request.data.get("duration", None)
        faculty_id = request.data.get("faculty", None)
        level_id = request.data.get("level", None)
        affiliation_id = request.data.get("affiliation", None)
        discipline_ids = request.data.get("discipline", [])

        # Ensure required fields are not missing
        missing_fields = {}
        if not duration_id:
            missing_fields["duration"] = "This field is required."
        if not faculty_id:
            missing_fields["faculty"] = "This field is required."
        if not level_id:
            missing_fields["level"] = "This field is required."
        if missing_fields:
            raise serializers.ValidationError(missing_fields)

        # Retrieve objects from database
        try:
            duration = Duration.objects.get(id=duration_id)
            faculty = Faculty.objects.get(id=faculty_id)
            level = Level.objects.get(id=level_id)
            affiliation = Affiliation.objects.get(id=affiliation_id) if affiliation_id else None
            # disciplines = Discipline.objects.filter(id__in=discipline_ids)
        except Duration.DoesNotExist:
            raise serializers.ValidationError({"duration": "Invalid ID."})
        except Faculty.DoesNotExist:
            raise serializers.ValidationError({"faculty": "Invalid ID."})
        except Level.DoesNotExist:
            raise serializers.ValidationError({"level": "Invalid ID."})
        except Affiliation.DoesNotExist:
            raise serializers.ValidationError({"affiliation": "Invalid ID."})
        # except Discipline.DoesNotExist:
            raise serializers.ValidationError({"discipline": "Invalid ID."})

        # Create course instance
        course = Course.objects.create(
            duration=duration, faculty=faculty, level=level, affiliation=affiliation, **validated_data
        )
        # course.discipline.set(disciplines)
        if isinstance(discipline_ids, str):
            discipline_ids = [int(id) for id in discipline_ids.split(",") if id.strip().isdigit()]
        elif isinstance(discipline_ids, list):
            discipline_ids = [int(id) for id in discipline_ids if isinstance(id, int)]
            
        disciplines = Discipline.objects.filter(id__in=discipline_ids)
        
        course.discipline.set(disciplines)
            


        # Extract curriculum files from request.FILES
        uploaded_files = [
            request.FILES[key] for key in request.FILES if key.startswith("curriculum_file_upload[")
        ]

        # Save multiple curriculum files
        for file in uploaded_files:
            if isinstance(file, InMemoryUploadedFile):  # Ensure valid file
                CourseCurriculumFile.objects.create(course=course, curriculum_file_upload=file)

        return course

    def update(self, instance, validated_data):
        """Handles updating a course with multiple curriculum file uploads"""
        request = self.context.get("request")

        # Extract required foreign key fields from request.data
        duration_id = request.data.get("duration", None)
        faculty_id = request.data.get("faculty", None)
        level_id = request.data.get("level", None)
        affiliation_id = request.data.get("affiliation", None)
        discipline_ids = request.data.get("discipline", [])
        
        if isinstance(discipline_ids, str):
            discipline_ids = [int(id) for id in discipline_ids.split(",") if id.strip().isdigit()]
        elif isinstance(discipline_ids, list):
            discipline_ids = [int(id) for id in discipline_ids if isinstance(id, int)]

        if duration_id:
            instance.duration = Duration.objects.get(id=duration_id)
        if faculty_id:
            instance.faculty = Faculty.objects.get(id=faculty_id)
        if level_id:
            instance.level = Level.objects.get(id=level_id)
        if affiliation_id:
            instance.affiliation = Affiliation.objects.get(id=affiliation_id) if affiliation_id else None
        if discipline_ids:
            instance.discipline.set(Discipline.objects.filter(id__in=discipline_ids))

            
        
        
            
        many_to_many_fields = {"discipline"}

        for attr, value in validated_data.items():
            if attr not in many_to_many_fields: 
                setattr(instance, attr, value)
        instance.save()

        # Extract curriculum files from request.FILES
        uploaded_files = [
            request.FILES[key] for key in request.FILES if key.startswith("curriculum_file_upload[")
        ]

        # Save new curriculum files
        for file in uploaded_files:
            if isinstance(file, InMemoryUploadedFile):  # Ensure valid file
                CourseCurriculumFile.objects.create(course=instance, curriculum_file_upload=file)

        return instance