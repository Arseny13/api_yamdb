
from django.urls import include, path
from rest_framework import routers

from . import views
from .views import (APIUser, CategoryViewSet, GenreViewSet, TitleViewSet,
                    UserViewSet, get_token, send_mail)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    views.ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)

router_v1.register('users', UserViewSet)

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/auth/signup/', send_mail, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router_v1.urls)),
]
