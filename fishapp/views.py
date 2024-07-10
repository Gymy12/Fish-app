from django.shortcuts import render
from .models import Category, Product, Banner, ProductAttribute
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.db.models import Max, Min
from django.template.loader import render_to_string
from Aquareach.credentials import PHONE_NUMBER

from .payments import pay_and_push


def home(request: HttpRequest):
    banners = Banner.objects.all().order_by("-id")
    data = Product.objects.filter(is_featured=True).order_by("-id")
    return render(request, "index.html", {"data": data, "banners": banners})


def about(request: HttpRequest):
    return render(request, "about.html")


def contacts(request: HttpRequest):
    return render(request, "contacts.html")


def category_list(request: HttpRequest):
    data = Category.objects.all().order_by("-id")
    return render(request, "category_list.html", {"data": data})


def product_list(request: HttpRequest):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by("-id")[:3]
    min_price = ProductAttribute.objects.aggregate(Min("price"))
    max_price = ProductAttribute.objects.aggregate(Max("price"))

    return render(
        request,
        "product_list.html",
        {
            "data": data,
            "total_data": total_data,
            "min_price": min_price,
            "max_price": max_price,
        },
    )


def category_product_list(request: HttpRequest, cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by("-id")

    return render(
        request,
        "category_product_list.html",
        {
            "data": data,
        },
    )


def product_detail(request: HttpRequest, slug, id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[
        :4
    ]
    quantities = ProductAttribute.objects.filter(product=product).select_related(
        "quantity"
    )
    counts = ProductAttribute.objects.filter(product=product).values_list(
        "count", flat=True
    )
    return render(
        request,
        "product_detail.html",
        {
            "data": product,
            "related": related_products,
            "quantities": quantities,
            "counts": counts,
        },
    )


def search(request: HttpRequest):
    q = request.GET["q"]
    data = Product.objects.filter(title__icontains=q)
    return render(request, "search.html", {"data": data})


def filter_data(request: HttpRequest):
    categories = request.GET.getlist("category[]")
    quantities = request.GET.getlist("quantity[]")
    minPrice = request.GET["minPrice"]
    maxPrice = request.GET["maxPrice"]
    allProducts = Product.objects.all().order_by("-id").distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)

    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()

    if len(quantities) > 0:
        allProducts = allProducts.filter(
            productattribute__quantity__id__in=quantities
        ).distinct()
    t = render_to_string("ajax/product-list.html", {"data": allProducts})
    return JsonResponse({"data": t})


def load_more_data(request: HttpRequest):
    offset = int(request.GET["offset"])
    limit = int(request.GET["limit"])
    data = Product.objects.all().order_by("-id")[offset : offset + limit]
    t = render_to_string("ajax/product-list.html", {"data": data})
    return JsonResponse({"data": t})


def add_to_cart(request: HttpRequest):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET["id"])] = {
        "image": request.GET["image"],
        "title": request.GET["title"],
        "qty": request.GET["qty"],
        "price": request.GET["price"],
    }
    if "cartdata" in request.session:
        if str(request.GET["id"]) in request.session["cartdata"]:

            cart_data = request.session["cartdata"]
            cart_data[str(request.GET["id"])]["qty"] = int(
                cart_p[str(request.GET["id"])]["qty"]
            )
            cart_data.update(cart_data)
            request.session["cartdata"] = cart_data
        else:
            cart_data = request.session["cartdata"]
            cart_data.update(cart_p)
            request.session["cartdata"] = cart_data
    else:

        request.session["cartdata"] = cart_p
    return JsonResponse(
        {
            "data": request.session["cartdata"],
            "totalitems": len(request.session["cartdata"]),
        }
    )


def cart_list(request: HttpRequest):
    total_amt = 0
    if "cartdata" in request.session:
        for p_id, item in request.session["cartdata"].items():
            total_amt += int(item["qty"]) * float(item["price"])
        return render(
            request,
            "cart.html",
            {
                "cart_data": request.session["cartdata"],
                "totalitems": len(request.session["cartdata"]),
                "total_amt": total_amt,
            },
        )
    else:
        return render(
            request,
            "cart.html",
            {"cart_data": "", "totalitems": 0, "total_amt": total_amt},
        )


# Delete Cart Item
def delete_cart_item(request: HttpRequest):
    p_id = str(request.GET["id"])
    if "cartdata" in request.session:
        if p_id in request.session["cartdata"]:
            cart_data = request.session["cartdata"]
            del request.session["cartdata"][p_id]
            request.session["cartdata"] = cart_data
    total_amt = 0
    for p_id, item in request.session["cartdata"].items():
        total_amt += int(item["qty"]) * float(item["price"])
    t = render_to_string(
        "ajax/cart-list.html",
        {
            "cart_data": request.session["cartdata"],
            "totalitems": len(request.session["cartdata"]),
            "total_amt": total_amt,
        },
    )
    return JsonResponse({"data": t, "totalitems": len(request.session["cartdata"])})


def update_cart_item(request: HttpRequest):
    p_id = str(request.GET["id"])
    p_qty = request.GET["qty"]
    if "cartdata" in request.session:
        if p_id in request.session["cartdata"]:
            cart_data = request.session["cartdata"]
            cart_data[str(request.GET["id"])]["qty"] = p_qty
            request.session["cartdata"] = cart_data
    total_amt = 0
    for p_id, item in request.session["cartdata"].items():
        total_amt += int(item["qty"]) * float(item["price"])
    t = render_to_string(
        "ajax/cart-list.html",
        {
            "cart_data": request.session["cartdata"],
            "totalitems": len(request.session["cartdata"]),
            "total_amt": total_amt,
        },
    )
    return JsonResponse({"data": t, "totalitems": len(request.session["cartdata"])})


def checkout(request: HttpRequest):
    total_amt = 0
    if "cartdata" in request.session:
        for p_id, item in request.session["cartdata"].items():
            total_amt += int(item["qty"]) * float(item["price"])
        # return render(
        #     request,
        #     "checkout.html",
        #     {
        #         "cart_data": request.session["cartdata"],
        #         "totalitems": len(request.session["cartdata"]),
        #         "total_amt": total_amt,
        #     },
        # )
        
        user_phone = request.user.phone
        res = pay_and_push(request, user_phone, total_amt)
        print("MPESA: ", res.content.decode())
        return res

    else:
        return render(
            request,
            "checkout.html",
            {"cart_data": "", "totalitems": 0, "total_amt": total_amt},
        )
