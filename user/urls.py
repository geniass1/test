from django.urls import path
from user.views import Register, ChangeInfo, Login


urlpatterns = [
    path('reg/', Register.as_view(), name='reg'),
    path('login/', Login.as_view(), name='login'),
    path('change/', ChangeInfo.as_view(), name='change'),
]

