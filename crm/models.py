from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^(\+?\d{1,3}[- ]?)?\d{3,15}$',
            message="Phone number must be in +1234567890 or 123-456-7890 format"
        )]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Auto-recalculate total before saving
        total = sum(p.price for p in self.products.all()) if self.pk else 0
        self.total_amount = total
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"
