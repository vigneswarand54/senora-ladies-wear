from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import registrationform
from accounts.models import accounts
from django.contrib import messages
from accounts.verify import send
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from order.models import Order, OrderProduct, Payment
from product.models import product, Variation
from .models import Cart, Cartitem,Delivery_address, wishlistitem,wishlist
from .forms import addressform,updateuserform
import requests

def register(request):
    if request.method == 'POST':
        form = registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phonenumber = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = accounts.objects.create_user(first_name=first_name, last_name=last_name,
                                                phone=phonenumber, email=email, username=username, password=password)
            user.phone = phonenumber
            request.session['phonenumber'] = phonenumber
            print(phonenumber)
            send(form.cleaned_data.get('phone'))
            user.save()
            messages.success(request, 'Registration successful.')
            return redirect('otp')
        else:
            messages.warning(request, 'passwords does not match')
            return redirect('register')
    else:
        form = registrationform()
    context = {
        'form': form,
    }
    return render(request, 'customer/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password,is_superadmin=False)
        if user is not None:
            try:
                print('entering inside try block') 
                cart = Cart.objects.get(cart_id=_cart_id(request)) 
                is_cart_item_exists = Cartitem.objects.filter(cart=cart).exists
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    Cart_item = Cartitem.objects.filter(cart=cart)
                    # getting the product variations by cart id
                    for item in Cart_item:
                        product_variation = []
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    
                    # gets the cart item from the user to access their product variations
                    cart_item = Cartitem.objects.filter( user=user)
                    existing_var_list= []
                    item_id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_var_list.append(list(existing_variation))
                        item_id.append(item.id)
                    
                    for pv in product_variation:
                        if pv in existing_var_list:
                            # increase cart_item quantity
                            index = existing_var_list.index(pv)
                            id = item_id[index]
                            item = Cartitem.objects.get(id=id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = Cartitem.objects.filter(cart=cart)
                            for item in Cart_item:
                                item.user = user
                                item.save() 
            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are logged in")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('query =',query)
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
            
        else:

            messages.error(request, 'invalid login credentials')
            return redirect('login')
    else:
        return render(request, 'customer/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('home')


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    current_user = request.user
    product_to_cart   = product.objects.get(id=product_id)
    # if user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method =='POST':
            for item in request.POST:
                key   = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product_to_cart,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = Cartitem.objects.filter(product=product_to_cart,user=current_user).exists
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(product=product_to_cart, user=current_user)
            
            # existing_variation -> database
            # current_variation -> product_variation
            # item_id -> database
            existing_var_list= []
            item_id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_var_list.append(list(existing_variation))
                item_id.append(item.id)
            print(existing_var_list)
            
            if product_variation in existing_var_list:
                # increase cart_item quantity
                index = existing_var_list.index(product_variation)
                id = item_id[index]
                item = Cartitem.objects.get(product=product_to_cart,id=id)
                item.quantity += 1
                item.save()
                
            else:
                # add new cart_item
                item = Cartitem.objects.create(product=product_to_cart, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = Cartitem.objects.create(
                product     =   product_to_cart,
                quantity    =   1,
                user        =   current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    
    #if the user is not authenticated
    else:    
        product_variation = []
        if request.method =='POST':
            for item in request.POST:
                key   = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product_to_cart,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = Cartitem.objects.filter(product=product_to_cart,cart=cart).exists
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(product=product_to_cart, cart=cart)
            
            # existing_variation -> database
            # current_variation -> product_variation
            # item_id -> database
            existing_var_list= []
            item_id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_var_list.append(list(existing_variation))
                item_id.append(item.id)
            print(existing_var_list)
            
            if product_variation in existing_var_list:
                # increase cart_item quantity
                index = existing_var_list.index(product_variation)
                id = item_id[index]
                item = Cartitem.objects.get(product=product_to_cart,id=id)
                item.quantity += 1
                item.save()
                
            else:
                # add new cart_item
                item = Cartitem.objects.create(product=product_to_cart, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = Cartitem.objects.create(
                product     =   product_to_cart,
                quantity    =   1,
                cart        =   cart,
                user        =   current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

def remove_from_cart(request,product_id,cart_item_id):
    item = get_object_or_404(product,id = product_id)
    try:
        if request.user.is_authenticated:
            Cart_item=Cartitem.objects.get(product=item, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            Cart_item=Cartitem.objects.get(product=item,cart=cart,id=cart_item_id)
        if Cart_item.quantity > 1:
            Cart_item.quantity -= 1
            Cart_item.save()
        else:
            Cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    item = get_object_or_404(product,id = product_id)
    if request.user.is_authenticated:
        Cart_item=Cartitem.objects.get(product=item,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        Cart_item=Cartitem.objects.get(product=item,cart=cart,id=cart_item_id)
    Cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.all().filter(user=request.user , is_active=True).order_by('id')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
          
    context = {
        'total'     : total,
        'grandtotal': grand_total,
        'tax'       : tax,
        'quantity'  : quantity,
        'cart_items': cart_items,
    }
    return render(request, 'customer/shop-cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user , is_active=True).order_by('id')
            address = Delivery_address.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True).order_by('id')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (3 * total)/100
        grand_total = total + tax
    except Cartitem.DoesNotExist:
        pass
    
    
    context = {
        'total'     : total,
        'grandtotal': grand_total,
        'tax'       : tax,
        'quantity'  : quantity,
        'cart_items': cart_items,
        'address'   : address
    }
    return render(request, 'customer/checkout.html',context)

@login_required(login_url='login')
def save_address(request):
    if request.method == 'POST':
        form = addressform(request.POST)
        User = request.user
        if form.is_valid:
            if User.is_authenticated:
                user             = User
                firstname        = request.POST['firstname']
                lastname         = request.POST['lastname']
                addressfield_1   = request.POST['addressfield_1']
                addressfield_2   = request.POST['addressfield_2']
                city             = request.POST['city']
                state            = request.POST['state']
                country          = request.POST['country']
                post_code        = request.POST['post_code']
                phonenumber      = request.POST['phonenumber']
                email            = request.POST['email']
                
                address = Delivery_address.objects.create(
                    user=user,
                    firstname=firstname,
                    lastname=lastname,
                    addressfield_1=addressfield_1,
                    addressfield_2=addressfield_2,
                    city=city,
                    state=state,
                    country=country,
                    post_code=post_code,
                    phonenumber=phonenumber,
                    email=email,
                    )
                address.save()
                messages.success(request, "Address is saved")
                return redirect(checkout)
            else:
                return redirect(login)
    else:
        messages.info(request, "please enter the reqired information")
        return redirect(checkout)

@login_required(login_url='login')
def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create(request.user)
    return wishlist
   
@login_required(login_url='login')
def Wishlist(request):
    try:
          Wishlist = wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except wishlist.DoesNotExist:
            Wishlist = wishlist()
            Wishlist.wishlist_id=_wishlist_id(request) 
            Wishlist.save()
    try:
        if request.user.is_authenticated:
            wishlist_items = wishlistitem.objects.all().filter(user=request.user).order_by('id')
        else:
            Wishlist = wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = wishlistitem.objects.filter(wishlist=Wishlist).order_by('id')
        
    except ObjectDoesNotExist:
        pass
          
    context = {
        
        'wishlist_items': wishlist_items,
    }
    return render(request,'customer/wishlist.html',context)

@login_required(login_url='login')
def add_to_wishlist(request,product_id):
    current_user=request.user
    item = None
    try:
          Wishlist = wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except wishlist.DoesNotExist:
            Wishlist = wishlist()
            Wishlist.wishlist_id=_wishlist_id(request)
            Wishlist.save()
            
            
    product_to_wishlist   = product.objects.get(id=product_id)
    wishlist_items=wishlistitem.objects.all()
    
    for item in wishlist_items:
        if  product_to_wishlist == item:
            messages.warning(request,'This item is already in wishlist.')
            return redirect('wishlist')
        else:
            wishlist_item = wishlistitem()
            wishlist_item.product     =   product_to_wishlist
            wishlist_item.wishlist    =   wishlist.objects.get(wishlist_id=Wishlist)
            wishlist_item.user        =   current_user
            wishlist_item.save()
            return redirect('wishlist')

@login_required(login_url='login')      
def remove_from_wishlist(request,product_id,wishlist_item_id):
    item = get_object_or_404(product,id = product_id)
    if request.user.is_authenticated:
        wishlist_item=wishlistitem.objects.get(product=item,user=request.user,id=wishlist_item_id)
    else:
        Wishlist = wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_item=wishlistitem.objects.get(product=item,wishlist=Wishlist,id=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')
        
@login_required(login_url='login')
def user_dashboard(request):
    order_product = OrderProduct.objects.filter(user=request.user)
    order = Order.objects.filter(user = request.user)
    payment = Payment.objects.filter(user = request.user)
    user = accounts.objects.get(id=request.user.id)
    form=updateuserform(instance=user)
    if not request.user.is_superadmin:
        
        if request.method == 'POST':
            form=updateuserform(request.POST,instance=user)
            if form.is_valid():
                form.save()
                return redirect('user_dashboard')

    context = {
        'order':order,
        'order_product': order_product,
        'payment':payment,
        'form':form,
    }
    return render(request,'customer/user_details.html',context)

# def cancel_order(request,pk):
#     print(pk)
#     order = Order.objects.get(order_number=pk)
#     print(order)
#     if order.status != 'Completed':
#         print(order.status)
#         order.Status = 'Cancelled'
#         print(order.status)
#         order.save()
#         messages.success(request,'Product Cancellation processed.')
#     return redirect('user_dashboard')