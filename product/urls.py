from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home, name='home'),
    path('products/',views.products, name='products'),
    path('products/<slug:category_slug>/',views.products, name='products_by_category'),
    path('products/<slug:category_slug>/<slug:subcategory_slug>/',views.products, name='products_by_subcategory'),
    path('products/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',views.product_details, name='product_details'),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)