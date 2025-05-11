from django.test import TestCase
from .models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Test Product", price=100.00, stock=10)

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 100.00)