from .models import Product, Category, Quantity, ProductAttribute
from django.db.models import Min, Max


def get_filters(request):
    cats = (
        Product.objects.distinct().values("category__title", "category__id").distinct()
    )
    quantities = (
        ProductAttribute.objects.distinct()
        .values("quantity__unit", "quantity__id")
        .distinct()
    )
    minMaxPrice = ProductAttribute.objects.aggregate(Min("price"), Max("price"))

    data = {"cats": cats, "quantities": quantities, "minMaxPrice": minMaxPrice}

    return data
