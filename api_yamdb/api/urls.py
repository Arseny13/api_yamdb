from django.urls import include, path
from rest_framework import routers

from api.views import (
    ReviewViewSet, APIUser, CategoryViewSet,
    GenreViewSet, TitleViewSet, CommentViewSet,
    UserViewSet, get_token, send_code
)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

router_v1.register('users', UserViewSet, basename='users')

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

url_singup = [
    path('signup/', send_code, name='signup'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('v1/auth/', include(url_singup)),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router_v1.urls)),
]
