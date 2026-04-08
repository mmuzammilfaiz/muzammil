from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer
from .models import Product
from django.shortcuts import get_object_or_404
# Create your views here.
class ProductAPI(APIView):
    def post(self,request):
        serializer=ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors)
    def get_object(self,id):
        return get_object_or_404(Product,id=id)

    def get(self,request, id=None):
        # Agar ID di ho → single product
        if id is not None:
            products = self.get_object(id)
            serializer = ProductSerializer(products)
            return Response(serializer.data)
        products=Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)

