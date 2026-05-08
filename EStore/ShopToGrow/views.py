from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, BasePermission

from .models import Product, Category, OTP
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializer import ProductSerializer, CategorySerializer
from .serializer import ReviewSerializer
from .utils import generate_otp

from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import requests
from rest_framework_simplejwt.tokens import RefreshToken




# =========================
#  PERMISSION
# =========================
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
        



# =========================
# PRODUCT API
# =========================
class ProductAPI(APIView):
   # permission_classes = [IsAdminUser]
    
    

    '''def get_permissions(self):
        if self.request.method == 'GET': #put patch post
            return [AllowAny()]
        return [IsAdminUser()]'''

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk=None):
        if pk:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


# =========================
# PRICE FILTER
# =========================
class ProductPriceRangeAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        products = Product.objects.all()

        if min_price and max_price:
            products = products.filter(price__range=(min_price, max_price))
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# =========================
#  CATEGORY
# =========================
class CategoryView(APIView):
    #permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        category.delete()
        return Response({"message": "Category deleted"})


# =========================
# PRODUCTS BY CATEGORY
# =========================
class ProductByCategoryAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# =========================
#  AUTH (SESSION ONLY FOR TEACHING)
# =========================
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username & password required"}, status=400)

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response({"message": "Login successful"})

        return Response({"error": "Invalid credentials"}, status=401)


class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


# =========================
#  SIGNUP
# =========================
class SignupAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        User.objects.create_user(username=username, password=password, email=email)

        return Response({"message": "Signup successful"}, status=201)


# =========================
#  OTP SYSTEM
# =========================
class SendOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except:
            return Response({'error': 'User not found'}, status=404)

        OTP.objects.filter(user=user).delete()

        otp = generate_otp()
        OTP.objects.create(user=user, code=otp)

        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return Response({'message': 'OTP sent'})


class VerifyOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('otp')

        user = User.objects.get(email=email)
        otp = OTP.objects.filter(user=user, code=code).last()

        if not otp:
            return Response({'error': 'Invalid OTP'}, status=400)

        if otp.created_at < timezone.now() - timedelta(minutes=5):
            return Response({'error': 'OTP expired'}, status=400)

        otp.is_verified = True
        otp.save()

        return Response({'message': 'OTP verified'})


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('password')

        user = User.objects.get(email=email)
        otp = OTP.objects.filter(user=user, is_verified=True).last()

        if not otp:
            return Response({'error': 'OTP not verified'}, status=400)

        user.set_password(new_password)
        user.save()

        OTP.objects.filter(user=user).delete()

        return Response({'message': 'Password reset successful'})


# =========================
#  GOOGLE OAUTH
# =========================
class GoogleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Yeh URL frontend use karega user ko Google login page pe bhejne ke liye
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile"
        )
        return Response({"auth_url": auth_url})


class GoogleCallbackAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({"error": "Code not provided"}, status=400)

        # Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        token_data = token_response.json()

        if "error" in token_data:
            return Response({"error": token_data["error"]}, status=400)

        access_token = token_data.get("access_token")

        # Get user info from Google
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_info_response = requests.get(user_info_url, params={"access_token": access_token})
        user_info = user_info_response.json()

        email = user_info.get("email")
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")

        if not email:
            return Response({"error": "Email not found in Google account"}, status=400)

        # Find or create user
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": email.split('@')[0], # Use part of email as username
            "first_name": first_name,
            "last_name": last_name,
        })

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Redirect back to frontend with tokens (simple approach for this setup)
        frontend_dashboard_url = f"http://127.0.0.1:5500/frontend/dashboard.html?access={refresh.access_token}&refresh={refresh}&username={user.username}"
        from django.shortcuts import redirect
        return redirect(frontend_dashboard_url)

class AddReviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        

        # check if already reviewed
        if Review.objects.filter(user=request.user, product=product).exists():
            return Response({"error": "You already reviewed this product"}, status=400)
        
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    
class ProductReviewAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # related_name='reviews' 
        reviews = product.reviews.all().order_by('-created_at')

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ProductSearchAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title'] 
    
