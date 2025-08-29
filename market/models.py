from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    description = models.TextField(blank=True)
    harvest_date = models.DateField(default=date.today)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2)  # Allows fractional units
    unit = models.CharField(max_length=50, default='kg')  # e.g., kg, liter, bag
    location = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)  # comma-separated tags for filtering
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('farmer', 'slug', 'harvest_date')  # Unique per farmer

    @property
    def in_stock(self):
        return self.stock > 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Check uniqueness per farmer
            while Product.objects.filter(farmer=self.farmer, slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.harvest_date})"



# class Order(models.Model):
#     retailer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='orders-retailer'
#     )
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders-retailer')
#     quantity = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} by {self.retailer.username} for {self.product.name}"
