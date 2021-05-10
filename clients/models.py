from django.db import models

from utils.models import ActiveMixin


class Agent(ActiveMixin):
    representant = models.CharField(max_length=45)
    # company = models.ForeignKey()

    def __str__(self):
        return self.headline


class Balance(ActiveMixin):
    # company = models.ForeignKey
    # client = models.ForeignKey
    order_balance = models.CharField(max_length=45)
    facture_balance = models.CharField(max_length=45)
