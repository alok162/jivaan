from django.db import models

# Create your models here.


class Employee(models.Model):
    employee_code = models.CharField(primary_key=True, max_length=30)
    department = models.CharField(max_length=100)
    score = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
