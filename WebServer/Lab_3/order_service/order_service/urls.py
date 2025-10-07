from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
]
