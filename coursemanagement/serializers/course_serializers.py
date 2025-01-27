from rest_framework import serializers
from ..models import Duration, Faculty, Level, Discipline, Course
import ast
from django.core.exceptions import ValidationError


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

# Serializer for Discipline model
class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name'] 

class CourseListSerializers(serializers.ModelSerializer):
    # Nested serializers for related fields
    duration = DurationSerializer(read_only=True)
    faculties = FacultySerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    discipline = DisciplineSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseRetrieveSerializers(serializers.ModelSerializer):
    # Nested serializers for related fields
    duration = DurationSerializer(read_only=True)
    faculties = FacultySerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    discipline = DisciplineSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
         