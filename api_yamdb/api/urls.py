from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (send_mail,
get_token, UserViewSet,
APIUser)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/email/', send_mail, name='send_mail'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/users/me/', APIUser.as_view()),
]