from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

urlpatterns = [
      path('api-auth/', include('rest_framework.urls')),
      path('rest-auth/', include('rest_auth.urls')),
      path('admin/', admin.site.urls),
      path('user/', include(('user.urls', 'user'), namespace='user')),
      path('user-profile/', include(('user_profile.urls', 'user_profile'), namespace='user_profile')),
      path('user-actions/', include(('main.urls', 'user-actions'), namespace='user-actions')),

      path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
