from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/',views.register, name='register' ),
    path('login/',views.login, name= 'login'),
    path('logout/',views.logout, name= 'logout'),
    path('cart/',views.cart, name='cart'),
    path('cart/add/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/<int:cart_item_id>/',views.remove_from_cart, name = 'remove_from_cart'),
    path('cart/remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item, name = 'remove_cart_item'),
    path('wishlist/',views.Wishlist, name = 'wishlist'),
    path('wishlist/add/<int:product_id>/',views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/<int:wishlist_item_id>/',views.remove_from_wishlist, name = 'remove_from_wishlist'),
    path('checkout/',views.checkout, name='checkout'),
    path('checkout/save_address',views.save_address, name='save_address'),
    path('dashboard/',views.user_dashboard, name='user_dashboard'),
    # path('order/cancel/<int:pk>/',views.cancel_order,name='cancel_order')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)