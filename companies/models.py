from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=70, null=False)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        response = f"Company: {self.id}, "
        response += f"Name: {self.name}, "
        response += f"active: {self.is_active}"

        return response

    class Meta:
        ordering = ['id']
