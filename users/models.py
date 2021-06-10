from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models

from utils.models import ActiveMixin, TimeStampedMixin


class UserManager(BaseUserManager):
    "Custom user manager"

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """Internal function to create and save a user
           with the given email and password"""

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create user who is NOT superuser"""

        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create user who is superuser"""

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)


class Permission(TimeStampedMixin, ActiveMixin):
    """Custom permission model"""

    codename = models.CharField(max_length=30,
                                verbose_name='codigo',
                                unique=True)

    description = models.CharField(max_length=100,
                                   verbose_name='descripcion')

    class Meta:
        ordering = ['codename', 'description']

    def __str__(self):
        return '%s | %s' % (self.codename, self.description)


class Role(TimeStampedMixin, ActiveMixin):
    """Custom role model"""

    name = models.CharField(max_length=10,
                            unique=True,
                            verbose_name='rol')

    permissions = models.ManyToManyField(Permission)

    class Meta:
        """Define the behavior of Model."""

        verbose_name = 'Role'
        verbose_name_plural = 'roles'
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self.name)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedMixin, ActiveMixin):
    """Custom user model to be used accross the app"""

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='correo electronico'
    )
    name = models.CharField(
        max_length=45,
        verbose_name='nombre'
    )
    last_name = models.CharField(
        max_length=45,
        verbose_name='apellido',
        default='none'
    )
    is_staff = models.BooleanField(
        default=False
    )

    roles = models.ManyToManyField(Role)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        """Return the representation in string"""
        return self.email

    def get_short_name(self):
        """The user is identified by their email address"""
        return self.email

    class Meta:
        """Define the behavior of Model."""

        ordering = ('email',)
