
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (send_mail,
get_token, UserViewSet,
APIUser)
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet)

router_v1 = SimpleRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/email/', send_mail, name='send_mail'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router_v1.urls)),
]


