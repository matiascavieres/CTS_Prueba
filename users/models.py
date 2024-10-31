from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    verification_token = models.UUIDField(unique=True, null=True, blank=True)
