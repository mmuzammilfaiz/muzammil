from django.urls import path
from .views import ProductAPI
from .views import CategoryAPI,ProductByCategoryAPI

urlpatterns = [   
    path('products/', ProductAPI.as_view()),
    path('products/<int:id>/', ProductAPI.as_view()),
    path('products/range/', ProductAPI.as_view()),
    path('category/',CategoryAPI.as_view()),
    path('category/<int:id>/',CategoryAPI.as_view()),
    path('products/category/<int:category_id>',ProductByCategoryAPI.as_view()),

]