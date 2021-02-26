from django.urls import path
from .views import UserPost, UserPostGet


urlpatterns = [
    path('posts/', UserPost.as_view(), name='user_posts_gets'),
    path('posts/<int:id>/', UserPostGet.as_view(), name='user_posts_post'),
]

