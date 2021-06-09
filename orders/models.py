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
