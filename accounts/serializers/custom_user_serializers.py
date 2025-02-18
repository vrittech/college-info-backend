from rest_framework import serializers
from django.contrib.auth import get_user_model
# from department.models import Department
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import check_password, make_password
from socialmedia.models import SocialMedia
from accounts.models import CustomUser as User
from collegemanagement.models import College
import ast


# User = get_user_model()

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

    # Handle comma-separated values (e.g., "4,5")
    if isinstance(value_to_convert_data, str) and "," in value_to_convert_data:
        parsed_list = [item.strip() for item in value_to_convert_data.split(",")]
        # Convert to integers if possible
        mutable_data[value_to_convert] = [int(item) if item.isdigit() else item for item in parsed_list]
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
    
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id','name', 'url', 'media', 'created_at', 'updated_at' ]  # Adjust fields as per your SocialMedia model
class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name', 'address']  # Adjust based on model fields
# class StaffSocialMediaSerializer(serializers.ModelSerializer):
#     social_media = SocialMediaSerializer(read_only=True)

#     class Meta:
#         model = StaffHaveSocialMedia
#         fields = ['social_media', 'social_media_url','created_at', 'updated_at']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "group"
        model = Permission
        fields = ['id', 'name', 'codename']
        

        
class GroupSerializer(serializers.ModelSerializer):
    # permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name']
        ref_name='user_groups'

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ['id','name']

class CustomUserReadSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(read_only = True)
    groups = GroupSerializer(many=True,read_only = True)
    # usersocial = StaffSocialMediaSerializer(many=True,read_only = True)
    class Meta:
        model = User
        fields = '__all__'
        
    

class CustomUserWriteSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False)
    # usersocial = StaffSocialMediaSerializer(many=True, required=False)
    
    def to_internal_value(self, data):
        """Convert groups input from string to list using str_to_list."""
        data = str_to_list(data, 'groups')  
        data = str_to_list(data, 'social_media') 
        return super().to_internal_value(data)
    

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        social_media_data = validated_data.pop('social_media', [])
        password = validated_data.pop('password', None)

        # Create user
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)

        # Assign groups
        group_ids = [group.id if hasattr(group, 'id') else group for group in groups]
        user.groups.set(group_ids)  

        # Assign social media (assuming it's ManyToMany)
        if social_media_data:
            user.social_media.set(social_media_data)

        user.save()
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', [])
        social_media_data = validated_data.pop('social_media', [])
        password = validated_data.pop('password', None)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        # Convert groups into primary keys if they are objects
        group_ids = [group.id if hasattr(group, 'id') else group for group in groups]
        instance.groups.set(group_ids)

        # Assign social media (if present)
        if social_media_data:
            instance.social_media.set(social_media_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        """Customize response to include detailed foreign key objects instead of just IDs."""
        data = super().to_representation(instance)

        # Include nested representations
        data['groups'] = GroupSerializer(instance.groups.all(), many=True).data
        data['college'] = CollegeSerializer(instance.college).data if instance.college else None
        data['social_media'] = SocialMediaSerializer(instance.social_media.all(), many=True).data
        
        return data

class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    # usersocial = StaffSocialMediaSerializer(many=True,read_only = True)
    groups = GroupSerializer(many=True,read_only = True)
    # department = DepartmentSerializer(read_only = True)
    class Meta:
        model = User
        fields =fields = '__all__'
        # ('roles', 'department', 'email', 'full_name', 'social_links', 'position', 'phone', 'avatar', 'professional_image', )

class CustomUserChangePasswordSerializers(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        # Check if current password is correct
        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect"})
        return data

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

   