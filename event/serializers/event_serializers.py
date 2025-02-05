from rest_framework import serializers
from ..models import Event, EventCategory, EventOrganizer, EventGallery
from django.db import transaction


# Serializer for EventCategory
class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'created_date_time', 'created_date', 'updated_date']

# Serializer for EventOrganizer
class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = ['id', 'name', 'image', 'link', 'is_show', 'created_date_time', 'created_date', 'updated_date']

# Serializer for EventGallery
class EventGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGallery
        fields = ['id', 'image', 'is_featured_image', 'created_date_time', 'created_date', 'updated_date']

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



class EventWriteSerializers(serializers.ModelSerializer):
    """
    Serializer for handling event creation and image uploads.
    Many-to-Many fields are assigned using IDs, while images are uploaded separately to `EventGallery`.
    """

    category = serializers.PrimaryKeyRelatedField(many=True, queryset=EventCategory.objects.all())
    organizer = serializers.PrimaryKeyRelatedField(many=True, queryset=EventOrganizer.objects.all())
    image = EventGallerySerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        """
        Handles creation of an Event and uploads images to the gallery.
        """
        # Extract Many-to-Many fields
        category_ids = validated_data.pop('category', [])
        organizer_ids = validated_data.pop('organizer', [])

        # Extract images from request FILES
        images_data = []
        for key, file in self.context['request'].FILES.items():
            if key.startswith('images['):  # Accepts multiple images
                images_data.append(file)

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
        Handles updating of an Event and uploads new images to the gallery.
        """
        # Extract Many-to-Many fields
        category_ids = validated_data.pop('category', None)
        organizer_ids = validated_data.pop('organizer', None)

        # Extract images from request FILES
        images_data = []
        for key, file in self.context['request'].FILES.items():
            if key.startswith('images['):  # Accepts multiple images
                images_data.append(file)

        # Update instance fields
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