from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
import ast
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile  
from ..models import Course, CourseCurriculumFile, Duration, Faculty, Level, Discipline, Affiliation



def str_to_list(data, value_to_convert):
    """
    Converts a string representation of a list into an actual list if necessary.
    
    Args:
        data (QueryDict or dict): The incoming data from the request.
        value_to_convert (str): The key in the data to convert.
    
    Returns:
        dict: The modified data with the specified key converted to a list if necessary.
    """
    try:
        # Make a mutable copy of data
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        value_to_convert_data = mutable_data.get(value_to_convert, None)
        
        # Skip conversion if data is already a list or contains Discipline instances
        if isinstance(value_to_convert_data, list):
            # Check if it's a list of Discipline objects; if so, skip conversion
            if all(isinstance(item, Discipline) for item in value_to_convert_data):
                return mutable_data
            # If it's a list of IDs or similar, also skip conversion
            return mutable_data

        # Only parse if value is a string
        if isinstance(value_to_convert_data, str):
            try:
                # Attempt to parse as JSON list
                variations = ast.literal_eval(value_to_convert_data)
                if isinstance(variations, list):
                    mutable_data[value_to_convert] = variations
                else:
                    raise ValidationError({
                        value_to_convert: "Input string does not represent a list."
                    })
            except (ValueError, SyntaxError):
                # If not JSON, split by comma
                disciplines = [item.strip() for item in value_to_convert_data.split(',') if item.strip()]
                mutable_data[value_to_convert] = disciplines
        return mutable_data
    except KeyError:
        # Return unchanged data if value_to_convert is not in the data
        return data
    
    

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
        fields = ['id', 'name','slug']  

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
    affiliation = serializers.PrimaryKeyRelatedField(
        queryset=Affiliation.objects.all(), required=False, write_only=True
    )
    duration = serializers.PrimaryKeyRelatedField(
        queryset=Duration.objects.all(), required=True, write_only=True
    )
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=True, write_only=True
    )
    level = serializers.PrimaryKeyRelatedField(
        queryset=Level.objects.all(), required=True, write_only=True
    )
    discipline = serializers.PrimaryKeyRelatedField(
        queryset=Discipline.objects.all(), many=True, required=True, write_only=True
    )

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
            disciplines = Discipline.objects.filter(id__in=discipline_ids)
        except Duration.DoesNotExist:
            raise serializers.ValidationError({"duration": "Invalid ID."})
        except Faculty.DoesNotExist:
            raise serializers.ValidationError({"faculty": "Invalid ID."})
        except Level.DoesNotExist:
            raise serializers.ValidationError({"level": "Invalid ID."})
        except Affiliation.DoesNotExist:
            raise serializers.ValidationError({"affiliation": "Invalid ID."})
        except Discipline.DoesNotExist:
            raise serializers.ValidationError({"discipline": "Invalid ID."})

        # Create course instance
        course = Course.objects.create(
            duration=duration, faculty=faculty, level=level, affiliation=affiliation, **validated_data
        )
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

        for attr, value in validated_data.items():
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