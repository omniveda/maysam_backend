import uuid
from django.db import models
from .user import User
from .product import Product

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
