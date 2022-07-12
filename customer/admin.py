from django.contrib import admin
from . import models

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
    
class CartitemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')
    

class Delivery_addressAdmin(admin.ModelAdmin):
    list_display = ('firstname','lastname','addressfield_1','addressfield_2','city','state','country','post_code','phonenumber','email')


# Register your models here.
admin.site.register(models.Cart,CartAdmin)
admin.site.register(models.Cartitem,CartitemAdmin)
admin.site.register(models.wishlist)
admin.site.register(models.wishlistitem)
admin.site.register(models.Delivery_address)