from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model): #for categories
    name=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.name
    
class Product(models.Model): #table for products
    title=models.CharField(max_length=255)
    price=models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    image=models.ImageField(upload_to='products/',null=True,blank=True)
 
    def __str__(self):
        return self.title
    

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

''' def __str__(self):
        return f"{self.user.username} - {self.code}"
    
     '''
     
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"
   

