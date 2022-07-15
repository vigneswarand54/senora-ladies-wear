from django.db import models
from django.urls import reverse
from django.db.models import Avg
from accounts.models import accounts


# category model

class category(models.Model):
    category_name = models.CharField( max_length=50)
    slug          = models.SlugField( max_length=100,unique=True)
    description   = models.TextField( max_length=250,blank=True)
    cat_image     = models.ImageField(upload_to='media\category_photos', blank=True,null=True)
    
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    
    def __str__(self):
        return self.category_name
    
# subcategory models
    
class subcategory(models.Model):
    subcategory      = models.CharField(max_length=200,unique=True,null=False)
    slug             = models.SlugField(max_length=200,unique=True,null=False)
    category         = models.ForeignKey(category, on_delete=models.CASCADE ,unique=False)
    
    def __str__(self):
        return '%s %s %s' % (self.category,str('-'), self.subcategory)
    
    def get_url(self):
        return reverse('products_by_subcategory',args=[self.category.slug,self.slug])
    
# product model
    
class product(models.Model):
    product_name            = models.CharField(max_length=200,unique=True)
    slug                    = models.SlugField(max_length=200,unique=True)
    description             = models.TextField(max_length=200,unique=True)
    price                   = models.IntegerField()
    thumbnail_image_1       = models.ImageField(upload_to='media/product_photos',default='product image',null=False)
    thumbnail_image_2       = models.ImageField(upload_to='media/product_photos',default='product image',null=True)
    thumbnail_image_3       = models.ImageField(upload_to='media/product_photos',default='product image',null=True)
    thumbnail_image_4       = models.ImageField(upload_to='media/product_photos',default='product image',null=True)
    stock                   = models.IntegerField()
    is_available            = models.BooleanField(default=True)
    category                = models.ForeignKey(category, on_delete=models.CASCADE)
    subcategory             = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    created_date            = models.DateTimeField(auto_now_add=True)
    modified_date           = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.subcategory.slug,self.slug])
    
    def averagereview(self):
        reviews = reviewrating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
 
    

# ## variation manager ## #

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)
   
# ## variation model ## #
    
variation_category_choice = (
    
    ('color','color'),
    ('size' ,'size')
)  
class Variation(models.Model):
    product             = models.ForeignKey(product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices= variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value
    
    
class reviewrating(models.Model):
    product         = models.ForeignKey(product,on_delete=models.CASCADE)
    user            = models.ForeignKey(accounts, on_delete=models.CASCADE)
    subject         = models.CharField(max_length=100,blank=True)
    review          = models.TextField(max_length=500,blank=True)
    rating          = models.FloatField()
    ip              = models.CharField(max_length=20,blank=True)
    status          = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)