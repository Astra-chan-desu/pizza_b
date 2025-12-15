from django.contrib import admin
from django.urls import path,include
from pizza_b.api import PizzaViewSet, UserViewSet, BranchViewSet, DriverViewSet, OrderViewSet, OrderItemSerializer
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

router_pizza = routers.DefaultRouter()
router_pizza.register('', PizzaViewSet)

router_users = routers.DefaultRouter()
router_users.register('users', UserViewSet)

router_branches = routers.DefaultRouter()
router_branches.register('branches', BranchViewSet)

router_drivers = routers.DefaultRouter()
router_drivers.register('drivers', DriverViewSet)

router_orders = routers.DefaultRouter()
router_orders.register('orders', OrderViewSet)

urlpatterns = [
    path('pizzas/', include(router_pizza.urls)),
    path('users/', include(router_users.urls)),
    path('branches/', include(router_branches.urls)),
    path('drivers/', include(router_drivers.urls)),
    path('orders/', include(router_orders.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
