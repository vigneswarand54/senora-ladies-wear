from django.contrib import admin
from . import models

# Register your models here.


class productAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'category', 'subcategory', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


class categoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}


class subcategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory', 'slug', 'category')
    prepopulated_fields = {'slug': ('subcategory',)}


class variationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active')
    list_editable= ('is_active',)
    
    list_filter = ( 'variation_category',
                    'variation_value', 'is_active', 'created_date',)
    
admin.site.register(models.category, categoryAdmin)
admin.site.register(models.product, productAdmin)
admin.site.register(models.subcategory, subcategoryAdmin)
admin.site.register(models.Variation,variationAdmin)
admin.site.register(models.reviewrating)
