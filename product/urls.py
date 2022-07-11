from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home, name='home'),
    path('home/',views.home, name='home'),
    path('products/',views.products, name='products'),
    path('products/<slug:category_slug>/',views.products, name='products_by_category'),
    path('products/<slug:category_slug>/<slug:subcategory_slug>/',views.products, name='products_by_subcategory'),
    path('products/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',views.product_details, name='product_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)