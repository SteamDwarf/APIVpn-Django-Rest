from django.urls import path, include, re_path
from apivpn.views import TodoView, GoogleLogin, api_root
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from dj_rest_auth.views import PasswordResetConfirmView
from apivpn.views import UserListView



urlpatterns = [
    path('', api_root),
    path('api/v1/users/', UserListView.as_view()),
    path('api/v1/', include("dj_rest_auth.urls")),
    path('api/v1/todos/', TodoView.as_view(), name='todos-list'),
    path('api/v1/registration/', RegisterView.as_view(), name='registration'),
    path('api/v1/auth/google/callback/', GoogleLogin.as_view(), name="google_login"),
    path('api/v1/todos', TodoView.as_view()),
    re_path(
        r'^api/v1/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path('api/v1/account-confirm-email/',
        VerifyEmailView.as_view(),
        name='account_confirm_email'
    ),
    re_path(
        r'^accounts/',
        include('allauth.urls'),
        name='socialaccount_signup'
    ) 
]

""" re_path(r'^api/v1/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
    PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'), """