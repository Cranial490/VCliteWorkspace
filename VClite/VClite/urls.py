"""VClite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from core_api.views import *
from core_api.models import VC_T_User



urlpatterns = [
    path('admin/', admin.site.urls),
    path('apiv0/', include('core_api.urls')),
    path('OTP/', include('phone_verify.urls')),
    #path('auth/', obtain_auth_token),
    url(r'^auth/obtain_token/', obtain_jwt_token),
    url(r'^auth/refresh_token/', refresh_jwt_token),
    url(r'^auth/verify_token/', verify_jwt_token),
    url(r'^user/(?P<username>[\w-]+)/update_user', UserPartialUpdateView.as_view(), name='user_partial_update'),
    url(r'^auth/reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    url(r'changePassword/(?P<username>[a-z0-9\-]+)/(?P<validation_key>[a-z0-9\-]+)/$',
        ResetPassword.as_view(), name='reset-request'),
]

