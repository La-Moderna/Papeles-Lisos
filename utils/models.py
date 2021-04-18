"""Model mixins"""
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


# Create your models here.
class TimeStampedMixin(models.Model):
    """Define 'created_date' and 'last_modified' fields"""

    created_date = models.DateTimeField(
        editable=False,
        blank=True,
        null=True,
        auto_now_add=True,
        verbose_name=_('created date')
    )

    last_modified = models.DateTimeField(
        editable=False,
        blank=True,
        null=True,
        auto_now=True,
        verbose_name=_('last modified')
    )

    class Meta:
        "abstract because is common information for the models"

        abstract = True


class JsonMixin(models.Model):
    data = JSONField(null=True, blank=True)

    class Meta:
        "abstract because is common information for the models"

        abstract = True
