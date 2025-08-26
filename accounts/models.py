from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    FARMER = 'farmer'
    RETAILER = 'retailer'
    ROLES = [
        (FARMER, 'Farmer'),
        (RETAILER, 'Retailer'),
    ]
    # user_type = models.CharField(max_length=20, choices=USER_TYPES, default='retailer')
    role = models.CharField(max_length=20, choices=ROLES)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
