from django.urls import path
from .views import ProductAPI, ProductPriceRangeAPI
from .views import CategoryView
from .views import ProductByCategoryAPI
from .views import LoginAPI,SignupAPI,LogoutAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SendOTP, VerifyOTP, ResetPassword
from .views import GoogleCallbackAPIView, GoogleLoginAPIView
from .views import AddReviewAPI,ProductReviewAPI,ProductSearchAPI



urlpatterns = [
path('products/', ProductAPI.as_view()),                              # POST  product , GET products
path('products/<int:pk>/', ProductAPI.as_view()),                     # GET/PUT/PATCH/DELETE by product id
path('products/range/', ProductPriceRangeAPI.as_view()),
# GET - price range filter


path('category/', CategoryView.as_view()), 
path('categories/<int:pk>/', CategoryView.as_view()),# GET/POST - categories
path('products/category/<int:pk>/', ProductByCategoryAPI.as_view()),

#SESSION BASE LOGIN
path('login/', LoginAPI.as_view()),
path('signup/', SignupAPI.as_view()),
path('logout/', LogoutAPI.as_view()),

#JWT LOGIN
path('api/login/', TokenObtainPairView.as_view(), name='login'),
path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),

#OTP SYSTEM
path('send-otp/', SendOTP.as_view()),
path('verify-otp/', VerifyOTP.as_view()),
path('reset-password/', ResetPassword.as_view()),
path('auth/google/', GoogleLoginAPIView.as_view(), name='google_login'),
path('auth/google/callback/', GoogleCallbackAPIView.as_view()),
path('products/<int:pk>/add-review/', AddReviewAPI.as_view()),
path('products/<int:pk>/reviews/', ProductReviewAPI.as_view()),
path('products/search/',ProductSearchAPI.as_view()),


]