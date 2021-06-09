from django.db import models

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Company(ActiveMixin):

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    company_id = models.CharField(
        max_length=4,
        unique=True
    )

    name = models.CharField(
        max_length=70
    )

    def __str__(self):
        """Return the representation in string"""
        return self.company_id
    class Meta:
        """Define the behavior of Model."""

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
