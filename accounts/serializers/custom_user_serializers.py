from rest_framework import serializers
from django.contrib.auth import get_user_model
# from department.models import Department
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import check_password, make_password
# from socialmedia.models import SocialMedia,StaffHaveSocialMedia
from accounts.models import CustomUser


User = get_user_model()

# class SocialMediaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SocialMedia
#         fields = ['id','name', 'url', 'media', 'created_at', 'updated_at' ]  # Adjust fields as per your SocialMedia model

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
    

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, data):
        # Check if the position already exists in another Career
        position = data.get('position')
        if position and CustomUser.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A user with this position already exists."})
        return data

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        social_media_data = validated_data.pop('social_media', [])
        password = validated_data.pop('password', None)

        # Create user
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.groups.set(groups)
        user.save()

        # # Create social media records
        # for sm_data in social_media_data:
        #     StaffHaveSocialMedia.objects.create(
        #         staff=user,
        #         social_media=sm_data['social_media'],
        #         social_media_url=sm_data['social_media_url']
        #     )

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
        instance.groups.set(groups)
        instance.save()

        # Update or create social media records
        # for sm_data in social_media_data:
        #     StaffHaveSocialMedia.objects.update_or_create(
        #         staff=instance,
        #         social_media=sm_data['social_media'],
        #         defaults={'social_media_url': sm_data['social_media_url']}
        #     )

        return instance

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

   