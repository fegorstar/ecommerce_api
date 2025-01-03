from rest_framework import serializers
from .models import Category, Product, Discount

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'final_price', 'stock_quantity', 'created', 'category']

    def get_final_price(self, obj):
        return Discount.calculate_final_price(obj)

    def validate_name(self, value):
        """
        Ensure the product name is unique.
        """
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("A product with this name already exists.")
        return value


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'product', 'discount_type', 'value']

    def validate(self, data):
        if data['discount_type'] == Discount.PERCENTAGE and (data['value'] <= 0 or data['value'] > 100):
            raise serializers.ValidationError("Percentage discount must be between 1 and 100.")
        if data['discount_type'] == Discount.FIXED and data['value'] <= 0:
            raise serializers.ValidationError("Fixed discount value must be greater than 0.")
        return data
