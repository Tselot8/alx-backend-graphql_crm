import os
import django
from decimal import Decimal
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from crm.models import Customer, Product, Order


def seed():
    Customer.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

    c1 = Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    c2 = Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")

    p1 = Product.objects.create(name="Laptop", price=Decimal("999.99"), stock=10)
    p2 = Product.objects.create(name="Mouse", price=Decimal("25.50"), stock=50)

    o1 = Order.objects.create(customer=c1, order_date=timezone.now())
    o1.products.add(p1, p2)
    o1.total_amount = sum(p.price for p in o1.products.all())
    o1.save()

    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed()
