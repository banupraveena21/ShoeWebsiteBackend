from django.urls import path
from . import views
from .views import ProductDetailAPIView, EnquiryCreateView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('routes/', views.get_routes),
    path('cart/count/', views.cart_count),
    path("about/", views.about_view, name="about"),
    path('products/', views.product_list, name='products'),
    path('categories/', views.category_list, name='category_list'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view() , name='product-detail'),
    path('enquiry/', EnquiryCreateView.as_view(), name='enquiry-create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    
]
