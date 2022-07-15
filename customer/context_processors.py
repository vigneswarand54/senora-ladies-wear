from .models import Cartitem,Cart, wishlist,wishlistitem
from .views import Wishlist, _wishlist_id, _cart_id


def counter(request):
    cart_count = 0
    wishlist_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart = Cart.objects.filter(cart_id =_cart_id(request))
            if request.user.is_authenticated:
                cart_items = Cartitem.objects.all().filter(user=request.user)
            else:
                cart_items = Cartitem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
            
        try:
                
            Wishlist = wishlist.objects.filter(wishlist_id =_wishlist_id(request))
            if request.user.is_authenticated:
                wishlist_items = wishlistitem.objects.all().filter(user=request.user)
            else:
                wishlist_items = wishlistitem.objects.all().filter(wishlist=Wishlist[:1])
            for wishlist_item in wishlist_items:
                wishlist_count += 1
        except wishlist.DoesNotExist:
            wishlist_count = 0
    return dict(cart_count=cart_count,
                wishlist_count=wishlist_count,
                wishlist_items=wishlist_items
                )
            
