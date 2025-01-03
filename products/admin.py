from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Discount


############################### CATEGORY ADMIN ###############################

class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('id', 'name', 'parent_name', 'description', 'subcategories_count', 'subcategories_list')
    search_fields = ('name', 'description', 'parent__name')
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('subcategories_count', 'subcategories_list')

    def parent_name(self, obj):
        """
        Display the parent category name.
        """
        return obj.parent.name if obj.parent else None
    parent_name.short_description = 'Parent Category'

    def subcategories_count(self, obj):
        """
        Displays the number of subcategories for a category.
        """
        return obj.subcategories.count()
    subcategories_count.short_description = 'Subcategories Count'

    def subcategories_list(self, obj):
        """
        Displays a comma-separated list of subcategories.
        """
        return ", ".join([subcategory.name for subcategory in obj.subcategories.all()])
    subcategories_list.short_description = 'Subcategories'

    def get_queryset(self, request):
        """
        Optimize queryset for admin list view.
        """
        return super().get_queryset(request).prefetch_related('subcategories', 'parent')


############################### PRODUCT ADMIN ###############################

class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """
    list_display = ('id', 'name', 'category', 'price', 'stock_quantity', 'created', 'discounted_price')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'created')
    ordering = ('-created',)
    readonly_fields = ('created', 'discounted_price')

    def discounted_price(self, obj):
        """
        Calculates the final price after applying the highest discount.
        """
        final_price = Discount.calculate_final_price(obj)
        return format_html(f'<span style="color: green;">${final_price:.2f}</span>') if final_price else "$0.00"
    discounted_price.short_description = 'Discounted Price'


############################### DISCOUNT ADMIN ###############################

class DiscountAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Discount model.
    """
    list_display = ('id', 'product', 'discount_type', 'value', 'effective_discount', 'product_price', 'discounted_price')
    search_fields = ('product__name',)
    list_filter = ('discount_type', 'product__category')
    ordering = ('-value',)

    def effective_discount(self, obj):
        """
        Display a human-readable effective discount.
        """
        if obj.discount_type == Discount.PERCENTAGE:
            return f"{obj.value}%"
        return f"${obj.value:.2f}"
    effective_discount.short_description = 'Effective Discount'

    def product_price(self, obj):
        """
        Display the original price of the product.
        """
        return f"${obj.product.price:.2f}"
    product_price.short_description = 'Product Price'

    def discounted_price(self, obj):
        """
        Display the final discounted price of the product.
        """
        final_price = Discount.calculate_final_price(obj.product)
        return format_html(f'<span style="color: green;">${final_price:.2f}</span>')
    discounted_price.short_description = 'Discounted Price'


############################### REGISTER MODELS ###############################

# Registering the models with their respective admin configurations.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Discount, DiscountAdmin)
