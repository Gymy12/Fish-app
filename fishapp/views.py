from django.shortcuts import render, get_object_or_404
from .models import Category, Product,Quantity,Count,Banner,ProductAttribute
from django.http import JsonResponse,HttpResponse
from django.db.models import Max,Min,Count,Avg
from django.template.loader import render_to_string
from django.db import models


# Create your views here.
def home(request):
    banners =Banner.objects.all().order_by('-id')
    data =Product.objects.filter(is_featured=True).order_by('-id')
    return render(request, 'index.html',{'data':data, 'banners':banners})

def category_list(request):
    data =Category.objects.all().order_by('-id')
    return render(request, 'category_list.html',{'data':data})



def product_list(request):
    total_data=Product.objects.count()
    data =Product.objects.all().order_by('-id')[:3]
    min_price =ProductAttribute.objects.aggregate(Min('price'))
    max_price =ProductAttribute.objects.aggregate(Max('price'))
    
    return render(request, 'product_list.html', 
                {
                      'data':data,
                      'total_data':total_data,
                      'min_price':min_price,
                      'max_price':max_price     
                    
                      

                }
                )

def category_product_list(request,cat_id):
        category=Category.objects.get(id=cat_id)
        data=Product.objects.filter(category=category).order_by('-id')
        
        return render(request,'category_product_list.html',
                    {
                                'data':data,
                    })




def product_detail(request, slug, id):
    product=Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    quantities = ProductAttribute.objects.filter(product=product).select_related('quantity')
    counts = ProductAttribute.objects.filter(product=product).values_list('count', flat=True)
    return render(request, 'product_detail.html', {
        'data': product,
        'related': related_products,
        'quantities':quantities,
        'counts':counts
    })


def search(request):
    q = request.GET['q']
    data =Product.objects.filter(title__icontains=q)
    return render(request, 'search.html',{'data':data})



def filter_data(request):
    categories = request.GET.getlist('category[]')
    quantities = request.GET.getlist('quantity[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts =Product.objects.all().order_by('-id').distinct()
    allProducts=allProducts.filter(productattribute__price__gte=minPrice)
    allProducts=allProducts.filter(productattribute__price__lte=maxPrice)


    
    if len(categories)>0:
          allProducts=allProducts.filter(category__id__in=categories).distinct()

    if len(quantities)>0:
          allProducts=allProducts.filter(productattribute__quantity__id__in=quantities).distinct()
    t=render_to_string('ajax/product-list.html', {'data':allProducts})
    return JsonResponse({'data':t})



def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t}
)


def add_to_cart(request):
    # Clear existing cart data if it exists
    if 'cartdata' in request.session:
        del request.session['cartdata']
    
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }

    if 'cartdata' in request.session:
        cart_data = request.session['cartdata']
        if str(request.GET['id']) in cart_data:
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
        else:
            cart_data.update(cart_p)
        request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p

    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})