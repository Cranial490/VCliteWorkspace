from django.urls import path
from django.conf.urls import include

from rest_framework import routers
from django.conf.urls import url
from .views import *

router = routers.DefaultRouter()

router.register('shares', ShareViewSet)
router.register('asks', AskViewSet)
router.register('bids', BidViewSet)
router.register('order', OrderViewSet)
router.register('trade', OrderQViewSet)
router.register('user', UserViewSet)
router.register('register', RegisterViewSet)
router.register('executed', OrderExecutedViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^user/(?P<username>[\w-]+)/update_user',
        UserPartialUpdateView.as_view(), name='user_partial_update'),
    #url(r'^user/getEmail/$', 'getEmail', name = 'getEmail'),
]
