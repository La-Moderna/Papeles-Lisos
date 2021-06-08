from django.db import models

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Company(ActiveMixin):
<<<<<<< HEAD

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=70)

    class Meta:
        """Define the behavior of Model."""

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
=======
    company_id = models.CharField(
        max_length=4,
        unique=True
    )

    name = models.CharField(
        max_length=70
    )
>>>>>>> d5f064d085e43a11b8f92c9861f286de624d0baa
