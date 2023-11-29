# restaurants/urls.py
from django.conf.urls.static import static
from django.urls import path

from quickBite import settings
from . import views as carrie_views

urlpatterns = [
    path('', carrie_views.home, name='home'),
    path('restaurants/', carrie_views.restaurant_list, name='restaurant_list'),
    path('display_restaurants/', carrie_views.display_restaurants, name='restaurant_list'),
    path('menu/<int:restaurant_id>/', carrie_views.menu_page, name='menu_page'),
    path('add_to_cart/<int:restaurant_id>/<int:menu_item_id>/', carrie_views.add_to_cart, name='add_to_cart'),
    path('view_cart/', carrie_views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', carrie_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', carrie_views.checkout, name='checkout'),
    path('your_orders/', carrie_views.your_orders, name='your_orders'),
    path('delete_order/<int:order_id>/', carrie_views.delete_order, name='delete_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

