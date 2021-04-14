from django.db import models

# Create your models here.
from utils.models import TimeStampedMixin

class Rol(models.Model):
    """Custom rol model to be used accross the app"""
    
    class Meta:
        """Define the behavior of the model"""
        
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ('id',)
        
    id = models.AutoField(
        primary_key=True,
        verbose_name = 'ID'
    )
    name = models.CharField(
        max_length = 254,
        blank = False,
        verbose_name = 'nombre'
    )
    is_active = models.BooleanField(
        default = False
    )
    clave = models.CharField(
        max_length = 254,
        unique = True,
        verbose_name = 'clave'
    )
       
        
    def __str__(self):
        """Return the representation in String"""
        return self.name
    
    def get_short_name(self):
        """The rol is identified by its id"""
        return self.name