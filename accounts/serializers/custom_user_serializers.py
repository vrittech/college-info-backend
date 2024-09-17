from rest_framework import serializers
from django.contrib.auth.models import Group,Permission
from ..models import CustomUser
from django.contrib.auth.hashers import make_password
from .. import roles
from ..utilities.permission import SecureFields

class CustomUserReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name =  "account serializers"
        model = CustomUser
        # fields = '__all__' 
        exclude = ['password']

class CustomUserReadLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name =  "CustomUserReadLimitedSerializer serializers"
        model = CustomUser
        fields = ['id','email','first_name','username',] 

class CustomUserReadLimitedSerializer_1(serializers.ModelSerializer):
    class Meta:
        ref_name =  "CustomUserReadLimitedSerializer serializers"
        model = CustomUser
        fields = ['id','email','first_name','username','last_name','role','getRoleName']


class CustomUserSerializer(serializers.ModelSerializer):
    
    def validate_password(self,value):#field level validation
        if len(value) < 5:
            raise serializers.ValidationError('Password must be 8 digit')
        return make_password(value) 
    
    def validate_role(self,value):#field level validation
        user = self.context['request'].user
        # print(user.is_authenticated)
        if not user.is_authenticated:
            if value == roles.USER:
                pass
            else:
                raise serializers.ValidationError("You can only set USER,PUBLISHER as role") 
        elif user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            return value
        elif user.is_authenticated and value!=roles.USER:
                raise serializers.ValidationError("You can only set USER as role") 
        return value
    
    def validate_is_verified(self,value):

        user = self.context['request'].user
        if user.is_authenticated:
            if user.role == roles.ADMIN:
                return value
            else:
                return False
        else:
            return False

    def validate_is_superuser(self,value):
        if value == True:
            raise serializers.ValidationError("You can not set USER as SYSTEM_ADMIN") 
        else:
            return False

    def validate(self, attrs):
        request = self.context.get('request')
        action = self.context['view'].action     

        if action == 'partial_update':
            old_password = request.data.get('old_password')  
            if old_password is not None:      
                instance = self.instance
                if not instance.check_password(old_password):
                    raise serializers.ValidationError("Password does not match")
            attrs['old_password_change_case'] = True
        return attrs        

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        try:
            if self.context['request'].method == 'PUT':
                extra_kwargs['password'] = {'required': False}
            return extra_kwargs
        except:
            pass
    
    class Meta:
        ref_name =  "accountWriteserializer"
        model = CustomUser
        fields = '__all__' 


    def get_fields(self):
        model_fields = super().get_fields()
        SecureFields(self,model_fields,['email','is_active','is_verified','role','provider','username','is_superuser'],['PATCH','PUT'],[roles.ADMIN,roles.SUPER_ADMIN])
        # SecureFields(self,model_fields,['provider'],['PATCH','PUT'],[]) #if empty [] it means it is striction for all
        return model_fields

class RoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    role_name = serializers.CharField()
    def to_representation(self, instance):
        return {'role_id': instance[0], 'role_name': instance[1]}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class GroupNamesSerializer(serializers.Serializer):
    group_names = serializers.ListField(child=serializers.CharField())

class PermissionGroupSerializer(serializers.Serializer):
    permission_id = serializers.IntegerField()
    groups = serializers.DictField(child=serializers.BooleanField())


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'phone', 'image', 'email']
    
  
    