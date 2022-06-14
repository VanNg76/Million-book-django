from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def books(self):
        return self.__books
    @books.setter
    def books(self, value):
        self.__books = value


    @property
    def total_value(self):
        return self.__total_value
    @total_value.setter
    def total_value(self, value):
        self.__total_value = value