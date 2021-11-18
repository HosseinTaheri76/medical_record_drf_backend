from django.urls import path
from .views import CreateUserApiView, LogoutApiView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('accounts/create/', CreateUserApiView.as_view(), name='create-user'),
    path('accounts/login/', obtain_auth_token, name='login-user'),
    path('accounts/logout/', LogoutApiView.as_view(), name='logout-user'),
]
