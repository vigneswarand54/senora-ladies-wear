from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from order.models import OrderProduct
from product.forms import reviewform
from product.models import product,category, reviewrating, subcategory
from customer.models import Cartitem,Cart, wishlist
from django.contrib.auth.decorators import login_required
from customer.views import _cart_id
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator



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
    Products = None
    products_count=0
    paged_products =None
    if 'q' in request.GET:
        q = request.GET['q']
        Products = product.objects.filter(Q(product_name__icontains=q)|Q(category__category_name__icontains=q)|Q(subcategory__subcategory__icontains=q)).order_by('id')
        paginator=Paginator(Products,6)
        page= request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count = Products.count()

        
    elif category_slug != None and subcategory_slug == None:
        categories = get_object_or_404(category,slug = category_slug)
        Products = product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(Products,6)
        page= request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count = Products.count()
        
    elif category_slug != None and subcategory_slug != None:
        categories = get_object_or_404(category,slug = category_slug)
        subcategories = get_object_or_404(subcategory, slug = subcategory_slug)
        Products = product.objects.filter(category=categories,subcategory=subcategories,is_available=True)
        paginator=Paginator(Products,6)
        page= request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count = Products.count()
    else:
        Products = product.objects.all().filter(is_available=True)
        paginator=Paginator(Products,6)
        page= request.GET.get('page')
        paged_products= paginator.get_page(page)
        products_count = Products.count()
        
    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'products/shop.html',context)


def product_details(request,category_slug,subcategory_slug,product_slug):
    wishlist_items = wishlist.objects.all()
    try:
        single_product=product.objects.get(
            category__slug=category_slug,subcategory__slug=subcategory_slug,slug=product_slug)
        in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as p:
        raise p
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
         orderproduct = None
         
    reviews = reviewrating.objects.filter(user = request.user , product_id = single_product.id ,status = True)
    review_count = reviews.count()
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct'  : orderproduct,
        'reviews'       : reviews,
        'review_count'  : review_count,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'products/product-details.html',context)

def submit_review(request,product_id):
    if 'user' in request.session:  
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            try:
                reviews = reviewrating.objects.get(user__id=request.user.id,product__id = product_id)
                form = reviewform(request.POST,instance=reviews)
                form.save()
                messages.success(request,'Thank you! Your review has been updated')
                return redirect(url)
            except reviewrating.DoesNotExist:
                form = reviewform(request.POST)
                if form.is_valid():
                    data = reviewrating()
                    data.subject =form.cleaned_data['subject']
                    data.review =form.cleaned_data['review']
                    data.rating =form.cleaned_data['rating']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.product_id = product_id
                    data.user_id = request.user.id
                    data.save()
                    messages.success(request,'Thank you! Your review has been submitted')
                    return redirect(url)
        else:  
             return redirect('url')    
    else:           
        return redirect('dashboard')