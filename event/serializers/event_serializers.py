from rest_framework import serializers
from ..models import Event, EventCategory, EventOrganizer, EventGallery
from django.db import transaction
import ast


# Serializer for EventCategory
class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'created_date_time', 'created_date', 'updated_date']

# Serializer for EventOrganizer
class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = '__all__'

# Serializer for EventGallery
class EventGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = '__all__'

# Serializer for listing event details (basic view)
class EventListSerializers(serializers.ModelSerializer):
    # Nested fields for related models (full object details)
    category = EventCategorySerializer(many=True,read_only=True)  # Full details of categories
    organizer = EventOrganizerSerializer(many=True,read_only=True)  # Full details of organizers
    image = EventGallerySerializer(many=True,read_only=True)  # Full details of gallery images
    
    class Meta:
        model = Event
        fields = '__all__'


# Serializer for retrieving complete event details (detailed view)
class EventRetrieveSerializers(serializers.ModelSerializer):
    category = EventCategorySerializer(many=True,read_only=True)  # Full details of categories
    organizer = EventOrganizerSerializer(many=True,read_only=True)  # Full details of organizers
    image = EventGallerySerializer(many=True,read_only=True)  # Full details of gallery images
    class Meta:
        model = Event
        fields = '__all__'



import ast

def str_to_list(data, value_to_convert):
    """
    Converts a string representation of a list into an actual list if necessary.
    Ensures that single values or comma-separated values are correctly converted into lists of integers.
    """
    try:
        mutable_data = data.dict()  # Convert QueryDict to standard dict if necessary
    except Exception:
        mutable_data = data

    value_to_convert_data = mutable_data.get(value_to_convert)

    if isinstance(value_to_convert_data, list):
        return mutable_data  # If already a list, return unchanged

    # If it's a comma-separated string, convert it to a list of integers
    if isinstance(value_to_convert_data, str):
        if ',' in value_to_convert_data:
            # Split the string by commas, strip spaces, and convert each part to an integer
            mutable_data[value_to_convert] = [int(x.strip()) for x in value_to_convert_data.split(',')]
        else:
            # If it's a single value, convert it to a list of one integer
            mutable_data[value_to_convert] = [int(value_to_convert_data.strip())]
        return mutable_data

    # If it's a single item (not a list or string), wrap it in a list
    if value_to_convert_data and not isinstance(value_to_convert_data, list):
        mutable_data[value_to_convert] = [value_to_convert_data]
        return mutable_data

    try:
        variations = ast.literal_eval(value_to_convert_data)  # Convert string to list
        mutable_data[value_to_convert] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({f'{value_to_convert}': str(e)}) from e



class EventWriteSerializers(serializers.ModelSerializer):
    """
    Serializer for handling event creation with multiple images.
    Uses `str_to_list()` to convert `category` and `organizer` from string to list.
    """

    category = serializers.PrimaryKeyRelatedField(many=True, queryset=EventCategory.objects.all())
    organizer = serializers.PrimaryKeyRelatedField(many=True, queryset=EventOrganizer.objects.all())

    class Meta:
        model = Event
        fields = '__all__'

    def to_internal_value(self, data):
        """
        Converts `category` and `organizer` from string to list using `str_to_list()`.
        """
        if data.get("category"):
            data = str_to_list(data, "category")

        if data.get("organizer"):
            data = str_to_list(data, "organizer")

        return super().to_internal_value(data)

    @transaction.atomic
    def create(self, validated_data):
        """
        Handles event creation and image uploads.
        """
        request = self.context.get("request")

        # Extract Many-to-Many fields
        category_ids = validated_data.pop("category", [])
        organizer_ids = validated_data.pop("organizer", [])

        # Extract multiple images from `images[0]`, `images[1]`, ...
        images_data = [file for key, file in request.FILES.items() if key.startswith("images[")]

        # Create the Event instance
        event = super().create(validated_data)

        # Assign Many-to-Many relationships
        event.category.set(category_ids)
        event.organizer.set(organizer_ids)

        # Save images in EventGallery
        for image_file in images_data:
            EventGallery.objects.create(event=event, image=image_file)

        return event

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Handles full (PUT) and partial (PATCH) updates for events.
        Supports new image uploads and Many-to-Many relationship updates.
        """
        request = self.context.get("request")

        # Extract Many-to-Many fields
        category_ids = validated_data.pop("category", None)
        organizer_ids = validated_data.pop("organizer", None)

        # Extract multiple images from `images[0]`, `images[1]`, ...
        images_data = [file for key, file in request.FILES.items() if key.startswith("images[")]

        # Update the event instance
        instance = super().update(instance, validated_data)

        # Update Many-to-Many relationships if provided
        if category_ids is not None:
            instance.category.set(category_ids)
        if organizer_ids is not None:
            instance.organizer.set(organizer_ids)

        # Save new images in EventGallery
        for image_file in images_data:
            EventGallery.objects.create(event=instance, image=image_file)

        return instance