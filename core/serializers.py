from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Role, ExtendedPermission

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='permission.name', read_only=True)
    codename = serializers.CharField(source='permission.codename', read_only=True)

    class Meta:
        model = ExtendedPermission
        fields = ('id', 'name', 'codename', 'description')


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(source='group.permissions', many=True, read_only=True)
    name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'display_name', 'description', 'permissions', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(source='groups', many=True, read_only=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'gender',
            'birth',
            'is_email_verified',
            'roles',
            'permissions'
        )
        read_only_fields = ('is_email_verified', 'roles', 'permissions')

    def get_permissions(self, obj):
        # Convert Permission objects to strings for JSON serialization
        permissions = obj.get_all_permissions()
        # Ensure all permissions are strings
        return [str(perm) for perm in permissions]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation', 'name', 'gender', 'birth')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirmation = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()


class RoleAssignmentSerializer(serializers.Serializer):
    role = serializers.CharField()
    user_id = serializers.IntegerField()


class PermissionAssignmentSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.CharField())
    role = serializers.CharField()

