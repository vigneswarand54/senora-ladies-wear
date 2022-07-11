from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from product.models import product,category, subcategory
from customer.models import Cartitem,Cart
from django.contrib.auth.decorators import login_required
from customer.views import _cart_id
from django.db.models import Q



# Create your views here.
def home(request):
    products = product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'products/home.html',context)


def products(request,category_slug=None,subcategory_slug=None):
    categories = None
    subcategories = None
    products = None
    products_count=0
    
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            products = product.objects.filter(Q(product_name__icontains=q)|Q(category__icontains=q)|Q(subcategory__icontains=q)).order_by('id')
        
    elif category_slug != None and subcategory_slug == None:
        categories = get_object_or_404(category,slug = category_slug)
        products = product.objects.filter(category=categories,is_available=True)
        products_count = products.count()
        
    elif category_slug != None and subcategory_slug != None:
        categories = get_object_or_404(category,slug = category_slug)
        subcategories = get_object_or_404(subcategory, slug = subcategory_slug)
        products = product.objects.filter(category=categories,subcategory=subcategories,is_available=True)
        products_count = products.count()
    else:
        products = product.objects.all().filter(is_available=True)
        products_count = products.count()
        
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'products/shop.html',context)


def product_details(request,category_slug,subcategory_slug,product_slug):
    try:
        single_product=product.objects.get(
            category__slug=category_slug,subcategory__slug=subcategory_slug,slug=product_slug)
        in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as p:
        raise p
    
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
    }
    return render(request, 'products/product-details.html',context)