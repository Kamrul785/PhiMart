from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category, Review, ProductImage
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from product.paginations import DefaultPagination 
from rest_framework.permissions import DjangoModelPermissions
from product.permissions import IsReviewAuthorOrReadOnly
from api.permission import IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema

class ProductViewSet(ModelViewSet):
    
    """
    API endpoint for managing products in the e-commercee store
    - Allows authenticated admin to create, update, and delete products
    - Allows user to browsse and filter prorduct
    - Support searching by name, description and Category
    - SUpport ordering by price and updated_at
    
    """
    
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()
    
    def list(self, request, *args, **kwargs):
        """ Retrieve all the products """
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Crearte a product by admin',
        operation_description='This allow an admin to create a product',
        request_body= ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        """ Only authenticated can create product """
        return super().create(request, *args, **kwargs)

class ProductImageViewsSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id = self.kwargs['product_pk'])
         
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs.get('product_pk')}
    