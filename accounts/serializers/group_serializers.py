from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
# from accounts.models import GroupExtension

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "group"
        model = Permission
        fields = ['id', 'name', 'codename']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    position = serializers.IntegerField(required=False)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permission_ids', 'position']

    # def validate_position(self, value):
    #     # Check if a group with this position already exists in GroupExtension
    #     if GroupExtension.objects.filter(position=value).exists():
    #         raise serializers.ValidationError("A group with this position already exists.")
    #     return value

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        position = validated_data.pop('position', None)

        # Create the Group instance
        group = Group.objects.create(**validated_data)
        group.permissions.set(permission_ids)

        # Create or update GroupExtension with the position
        # GroupExtension.objects.create(group=group, position=position or group.id)
        return group

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        position = validated_data.pop('position', None)

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        instance.permissions.set(permission_ids)


        return instance
