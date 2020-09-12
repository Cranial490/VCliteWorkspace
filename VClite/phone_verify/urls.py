# Third Party Stuff
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include
# phone_verify
from .api import VerificationViewSet

default_router = DefaultRouter(trailing_slash=False)
default_router.register("phone", VerificationViewSet, basename="phone")

urlpatterns = [
    path('', include(default_router.urls)),
]


#urlpatterns = list(default_router.urls)