from rest_framework import serializers
from .models import Product
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
class ProductSerializer(serializers.ModelSerializer):  # (better naming)
    class Meta:
        model = Product
        fields = '__all__'  

    def validate_price(self,value):
        if value < 0 :
            raise serializers.ValidationError("Product price must be Positive")
        return value
    def validate_title(self,value):
        if len(value) < 3 :
            raise serializers.ValidationError("Title must have greater length")
        
        return value