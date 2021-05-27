from django.db import models

from utils.models import ActiveMixin


class Company(ActiveMixin):
    company_id = models.CharField(
        max_length=4,
        unique=True
    )

    name = models.CharField(
        max_length=70
    )
