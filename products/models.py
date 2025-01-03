from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['parent']),  # Index for parent field
        ]


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['category']),  # Index for category field
        ]


class Discount(models.Model):
    PERCENTAGE = 'PERCENTAGE'
    FIXED = 'FIXED'
    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.discount_type} - {self.value}"

    @staticmethod
    def calculate_final_price(product):
        """Applies the highest discount to the product."""
        discounts = product.discounts.all()
        if not discounts.exists():
            return product.price
        max_discount = max(
            discounts, 
            key=lambda d: d.value if d.discount_type == Discount.FIXED else (product.price * d.value / 100)
        )
        if max_discount.discount_type == Discount.FIXED:
            return max(product.price - max_discount.value, 0)
        return max(product.price * (1 - max_discount.value / 100), 0)
