from companies.models import Company

from django.db import models

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class Warehouse(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    name = models.CharField(max_length=4, unique=True)
    description = models.CharField(
        max_length=100
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        """Return the representation in string"""
        return self.name


class Item(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    
    item_id = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=70)
    udVta = models.CharField(max_length=4)
    access_key = models.CharField(max_length=20)
    standard_cost = models.DecimalField(max_digits=15, decimal_places=4)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Miss M:N table with Inventory
    # Miss M:N table with OrderDetails
    def __str__(self):
        """Return the representation in string"""
        return str(self.item_id) if self.item_id else ''


class Inventory(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default='0'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        """Define the behavior of the model"""
        verbose_name = "Inventory"
        verbose_name_plural = 'Inventories'
