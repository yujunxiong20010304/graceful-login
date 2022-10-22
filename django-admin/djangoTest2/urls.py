from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from oAuth.views import UserInfoViewSet, UserViewSet, BookViewSet, UserCreateViewSet

router_V1 = routers.DefaultRouter()
router_V1.register('info', UserInfoViewSet)
router_V1.register('user_activate', UserCreateViewSet)
router_V1.register('user_create', UserCreateViewSet)
router_V1.register('users', UserViewSet)
router_V1.register('books', BookViewSet)

urlpatterns = [
    path('api/', include(router_V1.urls)),
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
