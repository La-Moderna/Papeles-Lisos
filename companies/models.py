from django.db import models

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Company(ActiveMixin):

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=70)

    class Meta:
        """Define the behavior of Model."""

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
