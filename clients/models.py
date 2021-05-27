from companies.models import Company

from django.db import models

from utils.models import ActiveMixin

from bulk_update_or_create import BulkUpdateOrCreateQuerySet

class Agent(ActiveMixin):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    representant = models.CharField(max_length=45)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Balance(ActiveMixin):
    # client = models.ForeignKey
    order_balance = models.CharField(max_length=45)
    facture_balance = models.CharField(max_length=45)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
