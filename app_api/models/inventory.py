from django.db import models

from .book import Book

class Inventory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

