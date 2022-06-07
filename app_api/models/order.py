from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

