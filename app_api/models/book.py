from django.db import models

from .author import Author
from .category import Category

class Book(models.Model):
    
    title = models.CharField(max_length=100)
    introduction = models.CharField(max_length=200)
    cover_image_url = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.FloatField()
    categories = models.ManyToManyField(Category, related_name="books")
