#  Entidades centrais do sistema de estudos


import uuid
from django.db import models
from django.conf import settings



class Subjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subjects"
    )
    name = models.CharField(max_length=100)
    color_hex = models.CharField(max_length=7, default="#6366F1")
    icon = models.CharField(max_length=50, default="")
    