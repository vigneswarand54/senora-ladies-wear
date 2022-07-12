from django.db import models
from accounts.models import accounts
from customer.models import Delivery_address
from product.models import Variation, product



# Create your models here.

class Payment(models.Model):
    user                = models.ForeignKey(accounts, on_delete=models.CASCADE)
    payment_id          = models.CharField(max_length=100)
    order_id            = models.CharField(max_length=100 ,null=True)
    payment_method      = models.CharField(max_length=100)
    amount_paid         = models.CharField(max_length=100)
    paid                = models.BooleanField(default=False)     
    created_at          = models.DateTimeField(auto_now_add=True)     
    
    def __str__(self):
        return self.payment_id
    
    
class Order(models.Model):
    
    STATUS  =   (
        ('New' , 'New'),
        ('Accepted' , 'Accepted'),
        ('Completed' , 'Completed'),
        ('Cancelled' , 'Cancelled'),
    )
    
    user                = models.ForeignKey(accounts, on_delete=models.SET_NULL,null=True)
    payment             = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number        = models.CharField(max_length=50)
    delivery_address    = models.ForeignKey(Delivery_address, on_delete=models.SET_NULL,null=True)
    order_note          = models.CharField(max_length=100,blank=True)
    order_total         = models.FloatField()
    tax                 = models.FloatField()
    status              = models.CharField(max_length=10,choices=STATUS,default='New')
    ip                  = models.CharField(blank=True,max_length=20)
    is_ordered          = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.order_number
    

class OrderProduct(models.Model):
    order               = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment             = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user                = models.ForeignKey(accounts, on_delete=models.CASCADE)
    product             = models.ForeignKey(product, on_delete=models.CASCADE)
    variation           = models.ManyToManyField(Variation,blank=True)
    quantity            = models.IntegerField()
    product_price       = models.FloatField()
    Ordered             = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.product.product_name