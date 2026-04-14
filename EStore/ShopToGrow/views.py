from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer
from .serializer import CategorySerializer
from .models import Product
from .models import Category
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
# Create your views here.

# product******************************************************************************************************************
class ProductAPI(APIView):
    # postapi----------------------------------------------------------------------------
    def post(self,request):
        serializer=ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors)
    def get_object(self,id):
        return get_object_or_404(Product,id=id)

    #PUT-Method---------------------------------------------------------------------------------
    def put(self,request,id):
        products=self.get_object(id)
        serializers=ProductSerializer(products,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    # patch----------------------------------------------------------------------------------
    def patch(self,request,id):
        products=self.get_object(id)
        serializers=ProductSerializer(products,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    def delete(self,request,id):
        products=self.get_object(id)
        products.delete()
        return Response({'message':"producd is deleted from the table"})
        
      
    
# get api------------------------------------------------------------------------------
    def get(self,request, id=None):
        # Agar ID di ho → single product
        if id is not None:
            products = self.get_object(id)
            serializer = ProductSerializer(products)
            return Response(serializer.data)
        
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        products = Product.objects.all()
        
        if min_price and max_price:
            products=Product.objects.filter(price__range=(min_price,max_price))
        elif min_price:
            products=Product.objects.filter(price__gte=min_price)
        elif max_price:
            products=Product.objects.filter(price__lte=max_price)
           
        if not products.exists():
            raise NotFound("No products found in this price range")
        

        serializers =ProductSerializer(products, many=True)     
        return Response(serializers.data)
    
class CategoryAPI(APIView):
    # Post-Method------------------------------------------------------------------------------
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
     #helper function-------------------------------------------------------------------------
    def get_object(self,id):
        return get_object_or_404(Category,id=id)

    #PUT-Method---------------------------------------------------------------------------------
    def put(self,request,id):
        category=self.get_object(id)
        serializers=CategorySerializer(category,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    #Patch-Method---------------------------------------------------------------------------------
    def patch(self,request,id):
        category=self.get_object(id)
        serializers=CategorySerializer(category,data=request.data, partial= True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)
    
    #Delete-Method------------------------------------------------------------------------------
    def delete(self,request, id):
        category=self.get_object(id)
        
        category.delete()
        return Response({"message":"category deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
    # Get-Method----------------------------------------------------------------------------------

    def get(self,request, id=None):

        # Agar ID di ho → single product
        if id is not None:
            try:
                category = Category.objects.get(id=id)
            except Category.DoesNotExist:
                raise Http404("Product not found")
            
            # category = self.get_object(id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        
        category= Category.objects.all()
        serializers =CategorySerializer(category, many=True)     
        return Response(serializers.data)