"""User API."""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users import serializers
from users.models import Permission, Role

from utils.mixins import (
    BaseGenericViewSet,
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from utils.routers import SingleObjectRouter


from app.urls import router

# User model
User = get_user_model()


class ProfileViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet,
                     BaseGenericViewSet):
    """Part of the Authentication Process"""

    serializer_class = serializers.UserProfileSerializer
    retrieve_serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        """Return the user in session."""
        return self.request.user


class AuthViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet,
                  BaseGenericViewSet):
    """Part of the Authentication Process"""

    serializer_class = serializers.AuthSerializer
    create_serializer_class = serializers.AuthSerializer
    retrieve_serializer_class = serializers.AuthResponseSerializer

    queryset = User.objects.all()

    permission_classes = [AllowAny]

    def get_object(self, email):
        """Return the user with given email"""
        queryset = self.get_queryset()
        return get_object_or_404(queryset, email=email)

    def create(self, request, *args, **kwargs):
        """User login with local credentials"""

        login_serializer = self.get_serializer(
            data=request.data
        )

        validation_response = login_serializer.is_valid(raise_exception=True)

        if validation_response:
            user = self.get_object(login_serializer.data['email'])

            response_serializer = self.get_serializer(
                user,
                action='retrieve'
            )

            return Response(response_serializer.data)
        return Response(
            login_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet,
                        BaseGenericViewSet):
    """Manage Creation of a User"""

    serializer_class = serializers.CreateUserSerializer
    create_serializer_class = serializers.CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Creation of the user depending if is Staff or not"""
        create_serializer = self.get_serializer(
            data=request.data,
            action='create'
        )
        if create_serializer.is_valid():
            # Revisar webservice de AD
            data = create_serializer.data

            email = data['email']
            password = data['password']
            extra_fields = {
                'name': data['name'],
                'last_name': data['last_name'],
                'is_staff': data['is_staff']
            }

            user = User.objects.create_user(
                email=email,
                password=password,
                **extra_fields
            )

            user.save()

            return Response(
                create_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                create_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class AddRoleUserViewSet(CreateModelMixin,
                         UpdateModelMixin,
                         viewsets.GenericViewSet,
                         BaseGenericViewSet):
    serializer_class = serializers.RetrieveRoleNameSerializer
    create_serializer_class = serializers.RetrieveRoleNameSerializer
    update_serializer_class = serializers.RetrieveUserRoleSerializer
    queryset = User.objects.filter(is_active=True)


class CreatePermissionViewset(CreateModelMixin,
                              ListModelMixin,
                              RetrieveModelMixin,
                              UpdateModelMixin,
                              DestroyModelMixin,
                              viewsets.GenericViewSet,
                              BaseGenericViewSet):
    """Manage creation of permission"""

    serializer_class = serializers.UserPermissionSerializer
    create_serializer_class = serializers.UserPermissionSerializer
    list_serializer_class = serializers.RetrievePermissionSerializer
    retrieve_serializer_class = serializers.RetrievePermissionSerializer
    update_serializer_class = serializers.UserPermissionSerializer
    queryset = Permission.objects.filter(is_active=True)


class CreateRoleViewset(CreateModelMixin,
                        ListModelMixin,
                        RetrieveModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet,
                        BaseGenericViewSet):

    serializer_class = serializers.UserRoleSerializer
    create_serializer_class = serializers.RolePermissionSerializer
    list_serializer_class = serializers.RetrieveRoleSerializer
    retrieve_serializer_class = serializers.RetrieveRoleSerializer
    update_serializer_class = serializers.UserRoleSerializer
    queryset = Role.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):

        validate_serializer = self.get_serializer(
            data=request.data,
        )
        validation_response = validate_serializer.is_valid(
            raise_exception=True)

        if validation_response:
            # Revisar webservice de AD
            data = validate_serializer.data
            rol = Role.objects.create(name=data['name'])
            permisos = data['permissions']
            for i in permisos:
                rol.permissions.add(i)
            rol.save()
            return Response(
                validate_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


router.register(
    r'auth',
    AuthViewSet,
    basename="auth",
)

router.register(
    r'me',
    ProfileViewSet,
    basename="me",
    router_class=SingleObjectRouter
)

router.register(
    r'users/create',
    CreateUserViewSet,
    basename="user_create"
)

router.register(
    r'roles',
    CreateRoleViewset,
    basename="role"
)

router.register(
    r'users/add-role',
    AddRoleUserViewSet,
    basename="user_role_add"
)

router.register(
    r'custom-permissions',
    CreatePermissionViewset,
    basename='permission'
)
