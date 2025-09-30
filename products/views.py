from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """
    قائمة جميع المنتجات
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, pk):
    """
    تفاصيل منتج محدد
    """
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'المنتج غير موجود'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """
    قائمة جميع الفئات
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products(request):
    """
    قائمة المنتجات المميزة
    """
    products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    """
    البحث عن المنتجات
    """
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

