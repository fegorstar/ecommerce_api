from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product, Discount


class ECommerceTests(APITestCase):
    """
    Test suite for the E-commerce API endpoints.
    """

    def setUp(self):
        """
        Set up test data for all test cases.
        """
        self.category = Category.objects.create(name="Electronics", description="Electronic items")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="Gaming Laptop",
            price=1000.00,
            stock_quantity=10,
        )

    ############################ CATEGORY TESTS ############################

    def test_list_categories(self):
        """
        Test retrieving all categories.
        """
        response = self.client.get("/api/categories/")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", json_response)
        self.assertEqual(json_response["message"], "Categories retrieved successfully")
        self.assertEqual(json_response["status"], status.HTTP_200_OK)

    ############################ PRODUCT TESTS #############################

    def test_list_products_with_pagination(self):
        """
        Test retrieving all products with pagination.
        """
        response = self.client.get("/api/products/")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", json_response)
        self.assertEqual(json_response["message"], "Products retrieved successfully")
        self.assertEqual(json_response["status"], status.HTTP_200_OK)

    def test_filter_products_by_category(self):
        """
        Test filtering products by category ID.
        """
        response = self.client.get(f"/api/products/?category_id={self.category.id}")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", json_response)
        self.assertEqual(json_response["message"], "Products retrieved successfully")
        self.assertEqual(json_response["status"], status.HTTP_200_OK)

    def test_create_product(self):
        """
        Test creating a new product.
        """
        data = {
            "name": "Phone",
            "description": "Smartphone",
            "price": 500.00,
            "stock_quantity": 15,
            "category": self.category.id,
        }
        response = self.client.post("/api/products/create/", data)
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["message"], "Product created successfully")
        self.assertEqual(json_response["status"], status.HTTP_201_CREATED)

    def test_create_product_with_duplicate_name(self):
        """
        Test creating a product with a duplicate name.
        """
        data = {
            "name": "Laptop",
            "description": "Another laptop",
            "price": 1500.00,
            "stock_quantity": 5,
            "category": self.category.id,
        }
        response = self.client.post("/api/products/create/", data)
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", json_response)
        self.assertEqual(json_response["status"], status.HTTP_400_BAD_REQUEST)

    def test_retrieve_product_details(self):
        """
        Test retrieving details of a specific product.
        """
        response = self.client.get(f"/api/products/{self.product.id}/")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", json_response)
        self.assertEqual(json_response["message"], "Product retrieved successfully")
        self.assertEqual(json_response["status"], status.HTTP_200_OK)

    ############################ DISCOUNT TESTS ############################

    def test_apply_discount(self):
        """
        Test applying a discount to a product.
        """
        data = {"product": self.product.id, "discount_type": "PERCENTAGE", "value": 10}
        response = self.client.post("/api/discounts/", data)
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["message"], "Discount applied successfully")
        self.assertEqual(json_response["status"], status.HTTP_201_CREATED)
