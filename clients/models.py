from companies.models import Company

from django.db import models

from utils.models import ActiveMixin


class Agent(ActiveMixin):
    representant = models.CharField(max_length=45)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Balance(ActiveMixin):
    # client = models.ForeignKey
    order_balance = models.CharField(max_length=45)
    facture_balance = models.CharField(max_length=45)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
