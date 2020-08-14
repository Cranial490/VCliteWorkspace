from django.urls import path
from django.conf.urls import include

from rest_framework import routers
from django.conf.urls import url
from .views import *
#from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
#from rest_framework_jwt.views import verify_jwt_token

router = routers.DefaultRouter()

router.register('shares', ShareViewSet)
router.register('asks', AskViewSet)
router.register('bids', BidViewSet)
router.register('order', OrderViewSet)
router.register('trade', OrderQViewSet)
router.register('user', UserViewSet)
router.register('register', RegisterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #url(r'^auth/obtain_token/', obtain_jwt_token),
    #url(r'^auth/refresh_token/', refresh_jwt_token),
    #url(r'^auth/verify_token/', verify_jwt_token),
    url(r'^user/(?P<username>[\w-]+)/update_user', UserPartialUpdateView.as_view(), name='user_partial_update'),
]
