from django.db import models
import csv


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, null=False)
    isActive = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.name}, Activo: {self.isActive}"

    class Meta:
        ordering = ['id']


class CompanyCsv:

    @staticmethod
    def load_csv(csv_url):

        # Open file
        with open(csv_url) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            line_count = 0
            for row in csv_reader:

                # Skip first line
                if line_count == 0:
                    line_count += 1
                else:
                    # Verify if id exist
                    query_companies = Company.objects.filter(id=row[0])

                    if query_companies.count() > 0:
                        # Get Company
                        company = Company.objects.get(id=row[0])

                        # Update Company
                        company.name = row[1]
                        company.save()
                    else:
                        # Create Company
                        company = Company.objects.create(
                            id=row[0],
                            name=row[1]
                        )
