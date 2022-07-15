from django.db import models
from django.urls import reverse
from accounts.models import accounts
from product.models import Variation, product
from accounts.models import accounts

# cart model

class Cart(models.Model):
    cart_id    = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class Cartitem(models.Model):
    user       = models.ForeignKey(accounts, on_delete=models.CASCADE, null=True)
    product    = models.ForeignKey(product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart       = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity   = models.IntegerField()
    is_active  = models.BooleanField(default=True)

    def total(self):
        return self.product.price * self.quantity
    
    def get_url(self):
        return reverse('product_details',args=[self.product.category.slug,self.product.subcategory.slug,self.product.slug])        
    
    def __unicode__(self):
        return self.product
    
class wishlist(models.Model):
    wishlist_id    = models.CharField(max_length=250,blank=True,unique=True)
    date_added     = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.wishlist_id
    
class wishlistitem(models.Model):
    user       = models.ForeignKey(accounts, on_delete=models.CASCADE, null=True)
    product    = models.ForeignKey(product, on_delete=models.CASCADE)
    wishlist   = models.ForeignKey(wishlist, on_delete=models.CASCADE, null=True)

    
    def get_url(self):
        return reverse('product_details',args=[self.product.category.slug,self.product.subcategory.slug,self.product.slug])        
    
    
class Delivery_address(models.Model):
    user            = models.ForeignKey(accounts, on_delete=models.SET_NULL,null=True)
    firstname       = models.CharField(max_length=50,null=False)
    lastname        = models.CharField(max_length=50,null=True)
    addressfield_1  = models.CharField(max_length=250,null=False)
    addressfield_2  = models.CharField(max_length=50,null=True)
    city            = models.CharField(max_length=50,null=False)
    state           = models.CharField(max_length=50,null=False)
    country         = models.CharField(max_length=50,null=False)
    post_code       = models.CharField(max_length=50,null=False)
    phonenumber     = models.CharField(max_length=50,null=False)
    email           = models.EmailField(max_length=50,null=False)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.user.username
    
    
   