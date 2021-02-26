from django.urls import path
from .views import UserPost


urlpatterns = [
    path('posts/<int:id>/', UserPost.as_view(), name='posts'),
]

