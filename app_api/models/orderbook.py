from django.db import models

from .book import Book
from .order import Order

class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordered_books")
    quantity = models.IntegerField()
