from companies.models import Company

from django.db import models

from utils.models import ActiveMixin


class Warehouse(ActiveMixin):

    class Meta:
        """Define the behavior of the model."""

        verbose_name = 'Almacen'
        verbose_name_plural = 'Almacenes'
    warehouse_name = models.CharField(max_length=4, unique=True)
    description = models.CharField(
        max_length=100
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Inventory(ActiveMixin):
    class Meta:
        """Define the behavior of the model"""
        verbose_name = "Inventario"
        verbose_name_plural = 'Inventarios'
    stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default='0'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )
    # articulo = models.ForeignKey(Articulo, on_delete= models.CASCADE)
