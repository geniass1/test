from django.urls import path
from .views import UserPost, UserPostGet, UserPostLikes, UserProfilePost, UserProfileGet


urlpatterns = [
    path('posts/', UserPost.as_view(), name='user_posts_gets'),
    path('posts/<int:id>/', UserPostGet.as_view(), name='user_posts_post'),
    path('likes/<int:id>/', UserPostLikes.as_view(), name='user_posts_likes'),
    path('change-user-profile/', UserProfilePost.as_view(), name='user-profile'),
    path('user-profile-get/<int:id>/', UserProfileGet.as_view(), name='user-profile-get'),
]

