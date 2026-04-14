from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=122)

    def __str__(self):
        return self.category


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title