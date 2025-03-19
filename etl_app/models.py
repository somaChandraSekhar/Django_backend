from django.db import models

class CompanyData(models.Model):
    name = models.CharField(max_length=100)
    revenue = models.IntegerField()
    profit = models.IntegerField()
    employees = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name