from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, EnquirySerializer, RegisterSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': response.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })




@api_view(['GET'])
def get_routes(request):
    routes = ['api/products/', 'api/users/']
    return Response(routes)


@api_view(['GET'])
def cart_count(request):
    # Simulate getting cart item count from session or DB
    count = request.session.get('cart_count', 1)  # Default to 1 for now
    return Response({'count': count})



# ABOUT VIEW #
@api_view(["GET"])
def about_view(request):
    data = {
        "about": (
            "StepUp is India’s largest sports and athleisure footwear brand. "
            "Incorporated in 2006, StepUp Activewear is one of the leading players "
            "in organized sports & casual footwear sector in India. Since 2016, the flagship "
            "brand 'StepUp', has been the largest sports and athleisure footwear brand in India, "
            "in both volume and value terms. The company’s products are available via an expansive "
            "Pan-India network of over 15,000 geo-tagged multi-brand retail stores, 35+ company-owned "
            "exclusive outlets, large format stores such as Walmart, Vishal Retail and Reliance Smart "
            "among others and all the leading e-commerce portals."
        ),
        "mission": (
            "At StepUp we craft shoes with care for everyone– men, women and kids, with an equal attention to "
            "detail, letting each shoe speak for itself. The world-class quality, trendy designs and affordable "
            "prices have captured the imagination of millions of people, across the country– making StepUp, an "
            "aspirational brand especially for – young adults, everyday performers and fashionistas."
        )
    }
    return JsonResponse(data)



@api_view(['GET'])
def product_list(request):
    qs = Product.objects.all().order_by('created_at')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    search = request.GET.get('search')
    if category:
        qs = qs.filter(category__slug=category)
    if brand:
        qs = qs.filter(brand__slug=brand)
    if search:
        qs = qs.filter(name__icontains=search)  # simple search
    serializer = ProductSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    cats = Category.objects.all()
    serializer = CategorySerializer(cats, many=True)
    return Response(serializer.data)



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'



class EnquiryCreateView(APIView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Enquiry submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)