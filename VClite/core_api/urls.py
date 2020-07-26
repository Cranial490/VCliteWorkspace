from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register('shares', ShareViewSet)
router.register('asks', AskViewSet)
router.register('bids', BidViewSet)
router.register('order', OrderViewSet)
router.register('trade', OrderQViewSet)
router.register('user', UserViewSet)
router.register('executed', OrderExecutedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
