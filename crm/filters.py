import django_filters
from .models import Customer, Product, Order

# ------------------------ Customer Filter ------------------------
class CustomerFilter(django_filters.FilterSet):
    nameIcontains = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    createdAtGte = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    createdAtLte = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Customer
        fields = ["nameIcontains", "createdAtGte", "createdAtLte"]


# ------------------------ Product Filter ------------------------
class ProductFilter(django_filters.FilterSet):
    nameIcontains = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    priceGte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    priceLte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stockGte = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    stockLte = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["nameIcontains", "priceGte", "priceLte", "stockGte", "stockLte"]


# ------------------------ Order Filter ------------------------
class OrderFilter(django_filters.FilterSet):
    totalAmountGte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    totalAmountLte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")
    orderDateGte = django_filters.DateFilter(field_name="order_date", lookup_expr="gte")
    orderDateLte = django_filters.DateFilter(field_name="order_date", lookup_expr="lte")
    customerName = django_filters.CharFilter(field_name="customer__name", lookup_expr="icontains")
    productName = django_filters.CharFilter(field_name="products__name", lookup_expr="icontains")

    class Meta:
        model = Order
        fields = [
            "totalAmountGte", "totalAmountLte",
            "orderDateGte", "orderDateLte",
            "customerName", "productName"
        ]
