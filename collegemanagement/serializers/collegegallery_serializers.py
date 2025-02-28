from rest_framework import serializers
from ..models import CollegeGallery, College

### ✅ College Serializer for nested relation ###
class CollegeSerializers(serializers.ModelSerializer):
    class Meta:
        model = College
        ref_name = 'CollegeGallerySerializers'
        fields = ['slug', 'id', 'name']


### ✅ Read Serializer (for Listing Multiple Galleries) ###
class CollegeGalleryListSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    # images = serializers.SerializerMethodField()  # Ensures `images` is the response key

    class Meta:
        model = CollegeGallery
        fields = '__all__'

    # def get_images(self, obj):
    #     """Returns a list of image URLs for consistency."""
    #     return [obj.image.url] if obj.image else []


### ✅ Read Serializer (for Retrieving a Single Gallery) ###
class CollegeGalleryRetrieveSerializers(serializers.ModelSerializer):
    college = CollegeSerializers(read_only=True)
    # images = serializers.SerializerMethodField()  # Ensures `images` is the response key

    class Meta:
        model = CollegeGallery
        fields = '__all__'

    # def get_images(self, obj):
    #     """Returns a list of image URLs for consistency."""
    #     return [obj.image.url] if obj.image else []


class CollegeGalleryWriteSerializers(serializers.ModelSerializer):
    # images = serializers.ListField(
    #     child=serializers.ImageField(), write_only=True, required=False
    # )  # Accept multiple image uploads

    class Meta:
        model = CollegeGallery
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')  # Auto-injected by Django

        images = []

        # Extract all image files dynamically
        for key, file_list in request.FILES.lists():
            if key.startswith("image["):
                images.extend(file_list)


        # Fetch college ID directly from request data
        college_id = request.data.get("college")
        if not college_id:
            raise serializers.ValidationError({"error": "College ID is required"})

        try:
            college = College.objects.get(id=college_id)
        except College.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid College ID"})

        if not images:
            raise serializers.ValidationError({"error": "No valid images uploaded"})

        gallery_instances = []

        # Create Gallery instances
        for image in images:
            try:
                gallery_instance = CollegeGallery.objects.create(image=image, college=college)
                gallery_instances.append(gallery_instance)
            except Exception as e:
                raise serializers.ValidationError({"error": "Failed to save image", "details": str(e)})

        

        # ✅ Instead of returning a list, return the first instance
        return gallery_instances[0] if gallery_instances else None

    def update(self, instance, validated_data):
        request = self.context.get('request')
       

        images = []

        # Extract all image files dynamically
        for key, file_list in request.FILES.lists():
            if key.startswith("image["):
                images.extend(file_list)


        # Update description only if it's in the request
        if 'description' in validated_data:
            instance.description = validated_data['description']
            instance.save()

        gallery_instances = []

        # Only add new images if they exist in the request
        if images:
            for image in images:
                try:
                    gallery_instance = CollegeGallery.objects.create(image=image, college=instance.college)
                    gallery_instances.append(gallery_instance)
                except Exception as e:
                    raise serializers.ValidationError({"error": "Failed to save image", "details": str(e)})



        # ✅ Return instance with updated images in `image` key
        return instance



    def to_representation(self, instance):
        """
        Converts image file paths into full URLs and supports lists.
        """
        request = self.context.get('request')  # Get request to generate full URL

        # ✅ If `instance` is a list, return a list of serialized data
        if isinstance(instance, list):
            return [
                {
                    "id": obj.id,
                    "image": request.build_absolute_uri(obj.image.url) if obj.image else None,
                    "college": obj.college.id if obj.college else None
                }
                for obj in instance
            ]

        # ✅ If `instance` is a single object, return a single object representation
        return {
            "id": instance.id,
            "image": request.build_absolute_uri(instance.image.url) if instance.image else None,
            "college": instance.college.id if instance.college else None
        }

