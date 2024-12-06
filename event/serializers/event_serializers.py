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


# Serializer for creating/updating event details (with full object serialization for related fields)
class EventWriteSerializers(serializers.ModelSerializer):
    # Nested serializers for related models (full object representation)
    category = EventCategorySerializer(many=True)  # For creating/updating full objects
    organizer = EventOrganizerSerializer(many=True)  # For creating/updating full objects
    gallery = EventGallerySerializer(many=True)  # For creating/updating full objects
    
    class Meta:
        model = Event
        fields = '__all__'
    
    def create(self, validated_data):
        # Handle the creation of related fields (many-to-many relationships)
        category_data = validated_data.pop('category')
        organizer_data = validated_data.pop('organizer')
        gallery_data = validated_data.pop('gallery')

        # Create the Event instance
        event = Event.objects.create(**validated_data)

        # Handle many-to-many relationships
        # Create related EventCategory, EventOrganizer, EventGallery
        for category in category_data:
            event.category.add(EventCategory.objects.create(**category))

        for organizer in organizer_data:
            event.organizer.add(EventOrganizer.objects.create(**organizer))

        for image in gallery_data:
            event.gallery.add(EventGallery.objects.create(**image))

        return event

    def update(self, instance, validated_data):
        # Handle the updating of related fields (many-to-many relationships)
        category_data = validated_data.pop('category', None)
        organizer_data = validated_data.pop('organizer', None)
        gallery_data = validated_data.pop('gallery', None)

        # Update fields that are present in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update many-to-many relationships
        if category_data is not None:
            instance.category.clear()  # Clear existing categories
            for category in category_data:
                instance.category.add(EventCategory.objects.create(**category))

        if organizer_data is not None:
            instance.organizer.clear()  # Clear existing organizers
            for organizer in organizer_data:
                instance.organizer.add(EventOrganizer.objects.create(**organizer))

        if gallery_data is not None:
            instance.gallery.clear()  # Clear existing gallery images
            for image in gallery_data:
                instance.gallery.add(EventGallery.objects.create(**image))

        # Save the updated instance
        instance.save()

        return instance
