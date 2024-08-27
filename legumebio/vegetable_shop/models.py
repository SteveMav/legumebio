from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Vegetable(models.Model):
       name = models.CharField(max_length=100)
       description = models.TextField()
       price = models.DecimalField(max_digits=10, decimal_places=2)
       stock = models.IntegerField()
       date_add = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return self.name

class Command(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    vegetable = models.ForeignKey('Vegetable', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    name_client = models.CharField(max_length=100)
    commune_client = models.CharField(max_length=200, default='Gombe')
    address_client = models.CharField(max_length=200)
    date_command = models.DateTimeField(default=datetime.now)
    statut = models.CharField(max_length=50, default='En cours')

    def __str__(self):
        return f"Commande de {self.name_client} - {self.vegetable.name}"    

class Suggestions(models.Model):
     name_user = models.CharField(max_length=200)
     email_user = models.CharField(max_length=200)
     suggestions = models.CharField(max_length=500)

     def __str__(self):
          return self.suggestions
    

