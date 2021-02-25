from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('api/token/', obtain_auth_token, name='obtain_auth_token'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
