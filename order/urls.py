from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('place_order/',views.place_order, name='place_order'),
    path('payment/status/',views.payment_status, name='payment_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)