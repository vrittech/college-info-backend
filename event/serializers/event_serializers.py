from rest_framework import serializers
from ..models import Event, EventCategory, EventOrganizer, EventGallery

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
    category = EventCategorySerializer(many=True)  # Full details of categories
    organizer = EventOrganizerSerializer(many=True)  # Full details of organizers
    gallery = EventGallerySerializer(many=True)  # Full details of gallery images
    
    class Meta:
        model = Event
        fields = '__all__'


# Serializer for retrieving complete event details (detailed view)
class EventRetrieveSerializers(serializers.ModelSerializer):
    # Nested fields for related models (full object details)
    category = EventCategorySerializer(many=True)
    organizer = EventOrganizerSerializer(many=True)
    gallery = EventGallerySerializer(many=True)  # Optional: For retrieving related images

    class Meta:
        model = Event
        fields = '__all__'


class EventWriteSerializers(serializers.ModelSerializer):
    # Accept IDs instead of nested objects for many-to-many relationships
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EventCategory.objects.all()
    )
    organizer = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EventOrganizer.objects.all()
    )
    gallery = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EventGallery.objects.all()
    )

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        # Extract related many-to-many field IDs
        category_ids = validated_data.pop('category', [])
        organizer_ids = validated_data.pop('organizer', [])
        gallery_ids = validated_data.pop('gallery', [])

        # Create the Event instance
        event = Event.objects.create(**validated_data)

        # Assign existing many-to-many objects using IDs
        event.category.set(category_ids)
        event.organizer.set(organizer_ids)
        event.gallery.set(gallery_ids)

        return event

    def update(self, instance, validated_data):
        # Extract related many-to-many field IDs
        category_ids = validated_data.pop('category', None)
        organizer_ids = validated_data.pop('organizer', None)
        gallery_ids = validated_data.pop('gallery', None)

        # Update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update many-to-many relationships only if provided
        if category_ids is not None:
            instance.category.set(category_ids)
        if organizer_ids is not None:
            instance.organizer.set(organizer_ids)
        if gallery_ids is not None:
            instance.gallery.set(gallery_ids)

        instance.save()
        return instance
