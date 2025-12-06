import uuid
from django.db import models
from .cart import Cart
from .product import Product
from .product_variation import ProductVariation

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
