from django.urls import path, include
from rest_framework import routers

from . import views


v1_router = routers.DefaultRouter()

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    views.ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
