from customer.models import Cartitem
from customer.views import cart
from .models import category,subcategory,product


def menu_links(request):
    links = category.objects.all()
    sublinks = subcategory.objects.all()
    productlinks = product.objects.all()
    return dict(links=links,
                sublinks=sublinks,
                productlinks=productlinks,
                )
    