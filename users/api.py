"""User API."""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users import serializers

from utils.mixins import BaseGenericViewSet
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

            response_serializer = self.retrieve_serializer_class(
                user
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
            data=request.data
        )
        if create_serializer.is_valid():
            # Revisar webservice de AD
            data = create_serializer.data

            email = data['email']
            password = data['password']
            extra_fields = {
                'phone': data['phone'],
                'last_name': data['last_name'],
                'name': data['name'],
                'is_staff': data['is_staff'],
                'is_active': False
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


router.register(
    r'auth',
    AuthViewSet,
    basename="auth",
)

router.register(
    r'me',
    ProfileViewSet,
    basename="user_me",
    router_class=SingleObjectRouter
)

router.register(
    r'users/create',
    CreateUserViewSet,
    basename="user_create",
)
