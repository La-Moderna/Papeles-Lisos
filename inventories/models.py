from companies.models import Company

from django.db import models

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class Item(ActiveMixin):
<<<<<<< HEAD

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.CharField(max_length=20, primary_key=True)
=======
    item_id = models.CharField(max_length=20, unique=True)
>>>>>>> d5f064d085e43a11b8f92c9861f286de624d0baa
    description = models.CharField(max_length=70)
    udVta = models.CharField(max_length=4)
    access_key = models.CharField(max_length=20)
    standard_cost = models.DecimalField(max_digits=15, decimal_places=4)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Miss M:N table with Inventory
    # Miss M:N table with OrderDetails
