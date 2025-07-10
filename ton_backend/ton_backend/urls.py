"""
URL configuration for ton_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers

from test_app.views import UserViewSet, GroupViewSet
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from apivpn.views import GoogleLogin
from apivpn.views import TodoView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include('apivpn.urls')),
    
    #path('api/v1/registration/account-confirm-email/<str:pk>/', VerifyEmailView.as_view(), name='account_email_verification_sent')
    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api/v1/', include('dj_rest_auth.urls')),
]

""" path("api/v1/", include("dj_rest_auth.urls")),
    path('api/v1/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/google/callback/', GoogleLogin.as_view(), name="google_login"),
    path('api/v1/todos', TodoView.as_view()),
    re_path(r'^api/v1/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    re_path(
        r'api/v1/account-confirm-email/(?P<key>[-:\w]+)/$',
        VerifyEmailView.as_view(),
        name='account_confirm_email'
    ),
    re_path(
        r'^accounts/',
        include('allauth.urls'),
        name='socialaccount_signup'
    ) """
