from clients.models import Client

from companies.models import Company

from django.db import models

from inventories.models import Item

from utils.models import ActiveMixin


class Order(ActiveMixin):
    obsOrder = models.CharField(max_length=100)
    ordenCompra = models.IntegerField(null=True)
    fechaOrden = models.CharField(max_length=10)
    fechaSolicitada = models.CharField(max_length=10)


class SalesOrder(ActiveMixin):
    status = models.CharField(max_length=15)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class OrderDetail(ActiveMixin):
    cantidad = models.IntegerField()
    udvta = models.CharField(max_length=4)
    precio = models.DecimalField(decimal_places=2, max_digits=10)
    posicion = models.CharField(max_length=15)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Authorization (ActiveMixin):
    vta = models.BooleanField(default=False)
    cst = models.BooleanField(default=False)
    suaje = models.BooleanField(default=False)
    grabado = models.BooleanField(default=False)
    pln = models.BooleanField(default=False)
    ing = models.BooleanField(default=False)
    cxc = models.BooleanField(default=False)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    # Missing FK "Orders"


class DeliveredQuantity(ActiveMixin):
    REG_TYPE_CHOICES = [
        (1, "Capturado"),
        (2, "Cancelado"),
        (3, "Facturado")
    ]
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='delivered_quantities'
    )
    order = models.BigIntegerField(unique=True)
    position = models.IntegerField()
    mov_date = models.DateField()
    time = models.BigIntegerField()
    sequence = models.IntegerField()
    reg_type = models.IntegerField(choices=REG_TYPE_CHOICES)
    quantity = models.FloatField()
    item = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        verbose_name='delivered_quantities'
    )

    class Meta:
        """Define the behavior of the model."""

        verbose_name = 'Cantidad Entregada'
        verbose_name_plural = 'Cantidades Entregadas'


class Invoice(ActiveMixin):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='invoices'
    )
    # Missing FK "Order" model
    invoice_number = models.BigIntegerField(unique=True)
    position = models.IntegerField()
    delivery = models.IntegerField()
    trans_type = models.CharField(max_length=4)
    item = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        verbose_name='invoices'
    )
    invoice_date = models.DateField()
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        verbose_name='invoices'
    )

    def __str__(self):
        return self.invoice_number

    class Meta:
        """Define the behavior of the model."""

        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'


class DeliverAddress(ActiveMixin):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='deliver_addresses'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        verbose_name='deliver_addresses'
    )
    del_address = models.CharField(max_length=4)
    nameA = models.CharField(max_length=50, null=True, blank=True)
    nameB = models.CharField(max_length=50, null=True, blank=True)
    nameC = models.CharField(max_length=50, null=True, blank=True)
    nameD = models.CharField(max_length=50, null=True, blank=True)
    nameE = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=5, null=True, blank=True)
    route_code = models.CharField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=3, null=True, blank=True)
    rfc = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        """Define the behavior of the model."""

        verbose_name = 'Direccion de Entrega'
        verbose_name_plural = 'Direcciones de Entrega'
