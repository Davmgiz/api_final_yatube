from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/v1/', include('api.urls')),
    path('api/v1/jwt/create/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/jwt/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/v1/jwt/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
