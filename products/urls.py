from django.urls import path
from .views import CategoryListView, ProductListView, ProductCreateView, ProductDetailView, DiscountViewSet

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('discounts/', DiscountViewSet.as_view({'post': 'create'}), name='discount-create'),
]
