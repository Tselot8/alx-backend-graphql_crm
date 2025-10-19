import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.core.validators import RegexValidator
from django.utils import timezone
from .models import Customer, Product, Order

# ------------------------
# GraphQL Object Types
# ------------------------

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


# ------------------------
# Mutations
# ------------------------

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        if phone:
            phone_validator = RegexValidator(
                regex=r'^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$',
                message="Invalid phone format. Use +1234567890 or 123-456-7890."
            )
            phone_validator(phone)

        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully!")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        created_customers = []
        errors = []

        for data in input:
            try:
                name = data.get("name")
                email = data.get("email")
                phone = data.get("phone")

                if not name or not email:
                    raise Exception("Name and email are required.")

                if Customer.objects.filter(email=email).exists():
                    raise Exception(f"Email '{email}' already exists.")

                if phone:
                    phone_validator = RegexValidator(
                        regex=r'^(\+?\d{10,15}|\d{3}-\d{3}-\d{4})$',
                        message="Invalid phone format. Use +1234567890 or 123-456-7890."
                    )
                    phone_validator(phone)

                customer = Customer.objects.create(name=name, email=email, phone=phone)
                created_customers.append(customer)

            except Exception as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.String(required=True)  # accept as string
        stock = graphene.Int(required=False, default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        from decimal import Decimal

        try:
            price = Decimal(price)
        except:
            raise Exception("Price must be a valid decimal number.")

        if price <= 0:
            raise Exception("Price must be positive.")
        if stock < 0:
            raise Exception("Stock cannot be negative.")

        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


from decimal import Decimal

class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids):
        customer = Customer.objects.get(pk=customer_id)
        products = Product.objects.filter(pk__in=product_ids)

        order = Order.objects.create(customer=customer)
        order.products.set(products)

        # ✅ Ensure total uses Decimal math
        total = sum([Decimal(p.price) for p in products])
        order.total_amount = total
        order.save()

        return CreateOrder(order=order)



# ------------------------
# Schema Definition
# ------------------------

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.select_related("customer").prefetch_related("products")


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
