from django.db import models

from utils.models import ActiveMixin


class Authorization (ActiveMixin):
    vta = models.BooleanField(default=False)
    cst = models.BooleanField(default=False)
    suaje = models.BooleanField(default=False)
    grabado = models.BooleanField(default=False)
    pln = models.BooleanField(default=False)
    ing = models.BooleanField(default=False)
    cxc = models.BooleanField(default=False)

    # Missing FK "Orders"
