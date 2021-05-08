# Python
import csv

# Django
from django.test import TestCase

# Models
from companies.models import Company, CompanyCsv


class CompanyTestFunction(TestCase):
    def setUp(self):
        self.createCSV = "companies/tests/files/createCompanies.csv"
        self.updateCSV = "companies/tests/files/updateCompanies.csv"
        self.createUpdateCSV = "companies/tests/files/createUpdateCompanies.csv"

    def test_create_by_cv(self):

        # Create Companies
        CompanyCsv.load_csv(self.createCSV)

        # Validate Data
        with open(self.createCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    company_data = Company.objects.get(id=row[0])
                    self.assertEqual(company_data.name, row[1])
                    line_count += 1

        # Check Companies created
        all_companies = Company.objects.all()
        self.assertEqual(all_companies.count(), 1)

    def test_update_companies(self):

        # Create Companies
        CompanyCsv.load_csv(self.createCSV)

        # Update Companies
        CompanyCsv.load_csv(self.updateCSV)

        # Load File
        with open(self.updateCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Validate Data
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    company_data = Company.objects.get(id=row[0])
                    self.assertEqual(company_data.name, row[1])
                    line_count += 1

        # Check Companies created
        all_companies = Company.objects.all()
        self.assertEqual(all_companies.count(), 1)

    def test_create_update_companies(self):

        # Create Companies
        CompanyCsv.load_csv(self.createCSV)

        # Update Companies
        CompanyCsv.load_csv(self.updateCSV)

        # Create and Update Companies
        CompanyCsv.load_csv(self.createUpdateCSV)

        # Load File
        with open(self.createUpdateCSV) as cvs_file:
            csv_reader = csv.reader(cvs_file, delimiter=',')

            # Validate Data
            csv_reader
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    company_data = Company.objects.get(id=row[0])
                    self.assertEqual(company_data.name, row[1])
                    line_count += 1

        # Check Companies created
        all_companies = Company.objects.all()
        self.assertEqual(all_companies.count(), 2)
