from django.db.models.deletion import DO_NOTHING
from companies.models import Company

from django.db import models

from inventories.models import Item, Warehouse

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Agent(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    representant = models.CharField(max_length=45)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class PriceList(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    DISCOUNT_LEVEL_CHOICES = [
        (1, 1),
        (2, 2)
    ]

    price_list_id = models.CharField(max_length=10)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='price_lists'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        related_name='price_lists'
    )
    discount_level = models.IntegerField(
        choices=DISCOUNT_LEVEL_CHOICES
    )
    cantOImp = models.BigIntegerField()
    price = models.FloatField()
    discount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.price_list_id

    class Meta:
        """Define the behavior of the model."""

        verbose_name = 'Lista de Precios'
        verbose_name_plural = 'Listas de Precios'


class Client(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    STATUS_CHOICES = [
        (1, "Cliente Normal"),
        (2, "Cliente Dudoso"),
        (3, "Cliente Bloqueado"),
        (4, "Cliente Potencia")
    ]
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='clients'
    )
    client_id = models.CharField(max_length=10, unique=True)
    nameA = models.CharField(max_length=50)
    nameB = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES)
    agent = models.ForeignKey(
        Agent,
        on_delete=models.DO_NOTHING,
        related_name='clients'
    )
    analist = models.CharField(max_length=10)
    currency = models.CharField(max_length=3)
    credit_lim = models.BigIntegerField()
    price_lists = models.ManyToManyField(
        PriceList,
        related_name='clients'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.DO_NOTHING,
        related_name='clients'
    )

    def __str__(self):
        return self.client_id

    class Meta:
        """Define the behavior of the model."""

        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Balance(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    
    # client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    client = models.CharField(max_length=10, default=0)
    order_balance = models.CharField(max_length=45)
    facture_balance = models.CharField(max_length=45)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
