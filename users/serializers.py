"""Serializer for user API."""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text

from rest_framework import serializers

from users.models import Permission as CustomPermission, Role, User


from utils.tokens import create_token


class UserPermissionSerializer(serializers.ModelSerializer):
    """Serializer for user permissions"""

    class Meta:
        """Define the class behavior"""

        model = Permission
        fields = '__all__'


class GroupPermissionSerializer(serializers.ModelSerializer):
    """Serializer for user groups."""

    permissions = UserPermissionSerializer(many=True)

    class Meta:
        """Define the class behavior"""

        model = Group
        fields = '__all__'


class SlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail(
                'does_not_exist',
                slug_name=self.slug_field,
                value=smart_text(data)
            )
        except (TypeError, ValueError):
            self.fail('invalid')


class UserPermissionCustomSerializer(serializers.ModelSerializer):

    """Serializer for permissions of a role"""
    class Meta:
        """Define behaivor"""
        model = CustomPermission
        fields = ['id', 'codename']


class RetrievePermissionSerializer(serializers.ModelSerializer):
    """Serializer for listing permissions"""

    def validate(self, data):
        try:
            CustomPermission.objects.get(id=data.get('id'))
        except CustomPermission.DoesNotExist:
            raise serializers.ValidationError("permission does not exist")
        return data

    class Meta:
        """Define behavior"""
        model = CustomPermission
        fields = [
            'id',
            'codename',
            'description'
        ]


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for user roles"""

    class Meta:
        """Define the class behaivor"""
        model = Role
        fields = '__all__'


class UserCustomRoleSerializer(serializers.ModelSerializer):
    """Serializer for user roles"""

    class Meta:
        """Define the class behaivor"""
        model = Role
        fields = ['id',
                  'name',
                  'permissions']


class RolePermissionSerializer(UserRoleSerializer):

    permissions = UserPermissionCustomSerializer(many=True, read_only=True)


class RoleCustomPermissionSerializer(UserCustomRoleSerializer):

    permissions = UserPermissionCustomSerializer(many=True, read_only=True)


class RetrieveRoleSerializer(serializers.ModelSerializer):
    """Serializer for listing and retrieving roles"""

    permissions = UserPermissionCustomSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'permissions'
        ]


class RetrieveRoleNameSerializer(serializers.ModelSerializer):
    """Serializer for listing and retrieving roles"""
    class Meta:
        model = Role
        fields = ['id',
                  'name']


class RetrieveUserRoleSerializer(serializers.ModelSerializer):
    """Serializer for listing and retrieving roles"""
    roles = SlugRelatedField(
        slug_field='id',
        many=True,
        queryset=Role.objects.filter(is_active=True)
    )

    class Meta:
        model = User
        fields = ['id',
                  'roles']


class UserProfileSerializer(serializers.ModelSerializer):
    """Profile serializer."""

    # user_permissions = UserPermissionSerializer(many=True)
    # groups = GroupPermissionSerializer(many=True)
    roles = RoleCustomPermissionSerializer(many=True)

    class Meta:
        """Define behaivor."""

        model = User
        fields = [
            'id',
            'email',
            # 'user_permissions',
            # 'groups',
            'roles'
        ]


class UserProfileCustomSerializer(serializers.ModelSerializer):
    """Profile serializer."""
    # due to custom permissions usage, the next line has to be commented
    # user_permissions = UserPermissionSerializer(many=True)
    roles = UserRoleSerializer(many=True)

    class Meta:
        """Define behaivor."""

        model = User
        fields = [
            'id',
            'email',
            'roles'
        ]


class RetrieveUserNameSerializer(serializers.ModelSerializer):
    """Profile serializer."""

    class Meta:
        """Define behaivor."""

        model = User
        fields = 'id'


class AddUserRoleSerializer(serializers.ModelSerializer):
    """Serializer for adding role to user"""
    roles = RetrieveRoleNameSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'roles'
        ]


class AuthSerializer(serializers.Serializer):
    """Serializer for Auth API when POST method is used"""

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        """Validation username, password and active status"""
        try:
            user = User.objects.get(email__exact=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError("credentials are not valid")

        if not user.check_password(data.get('password')):
            raise serializers.ValidationError("credentials are not valid")

        if not user.is_active:
            raise serializers.ValidationError(
                'The user has not been activated'
            )

        return data


class AuthResponseSerializer(serializers.ModelSerializer):
    """Serializer for Auth API when GET method is used"""

    token = serializers.SerializerMethodField()

    class Meta:
        """Define the behavior of Serializer"""

        model = User
        fields = [
            'email',
            'token'
        ]

    def get_token(self, obj):
        """Create token."""
        return create_token(obj)


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    is_staff = serializers.BooleanField(required=True)

    def validate_email(self, value):
        """Raise ValidationError if email already exists"""
        email = BaseUserManager.normalize_email(value)
        if User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError(
                "Email has already been registered"
            )
        else:
            return value


class RoleSerializer(serializers.ModelSerializer):
    """Role serializer"""

    class Meta:
        model = Role
        fields = '__all__'
