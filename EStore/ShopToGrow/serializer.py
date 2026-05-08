from rest_framework import serializers
from .models import Product,Category,Review
from django.db.models import Avg


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields='__all__'
        
    def get_average_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('rating'))['avg']
        
        
    def validate_price(self, value):
       if value < 0:
        raise serializers.ValidationError("Price can not be negative")
       return value
   
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title Should be more then 3 Character")
        return value
        
        
    def validate_description(self, value):
        if value:  
            if len(value) < 10:
                raise serializers.ValidationError("Description should contain atleat 10 characters")
        return value



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'product', 'created_at']
        