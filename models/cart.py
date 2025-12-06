import uuid
from django.db import models
from .user import User

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
