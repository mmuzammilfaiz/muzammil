from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):  # (better naming)
    class Meta:
        model = Product
        fields = '__all__'  