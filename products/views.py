from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from .models import Category, Product, Discount
from .serializers import CategorySerializer, ProductSerializer, DiscountSerializer
from utils.response_utils import success_response, error_response
from utils.pagination_utils import CustomPagination  # Import the custom pagination

############################### CATEGORY API ###############################

class CategoryListView(ListAPIView):
    """
    API to list all categories.
    Supports nested categories using prefetch_related for subcategories.
    """
    queryset = Category.objects.prefetch_related('subcategories').order_by('id')  # Ensure QuerySet is ordered
    serializer_class = CategorySerializer
    pagination_class = None  # Disable pagination for categories

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="Retrieve a list of all categories, including nested subcategories.",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return success_response("Categories retrieved successfully", data=serializer.data)


############################### PRODUCT API ###############################
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_summary="List Products",
        operation_description="Retrieve a list of products with pagination. Filter products by category using 'category_id' query parameter.",
        manual_parameters=[
            openapi.Parameter(
                'category_id', openapi.IN_QUERY, description="Filter products by category ID", type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Products retrieved successfully", data=serializer.data)

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        queryset = Product.objects.select_related('category').order_by('id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset





class ProductCreateView(CreateAPIView):
    """
    API to create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_summary="Create Product",
        operation_description="Create a new product by providing all required fields.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Product created successfully", data=serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response("Failed to create product", validation_errors=serializer.errors)


class ProductDetailView(RetrieveAPIView):
    """
    API to retrieve the details of a specific product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve Product Details",
        operation_description="Retrieve detailed information of a specific product by ID, including the final price after applying discounts.",
        responses={200: ProductSerializer}
    )
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer = self.get_serializer(product)
        return success_response("Product retrieved successfully", data=serializer.data)


############################### DISCOUNT API ###############################

class DiscountViewSet(ViewSet):
    """
    API to create a discount and apply it to a product.
    """
    @swagger_auto_schema(
        operation_summary="Apply Discount",
        operation_description="Create and apply a discount to a specific product. Provide the product ID, discount type (PERCENTAGE or FIXED), and the discount value.",
        request_body=DiscountSerializer,
        responses={201: DiscountSerializer}
    )
    def create(self, request):
        """
        Create a discount for a product.
        """
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Discount applied successfully", data=serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response("Failed to apply discount", validation_errors=serializer.errors)
