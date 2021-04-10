from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import Register, ChangeInfo


urlpatterns = [
    path('sign-up/', Register.as_view(), name='reg'),
    # path('sign-in/', Login.as_view(), name='login'),
    path('sign-in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('change/', ChangeInfo.as_view(), name='change'),
]

