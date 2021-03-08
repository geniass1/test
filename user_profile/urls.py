from django.urls import path
from .views import UserPost, UserPostGet, UserPostLikes, UserProfilePost, UserProfileGet,\
    UserPostDelete, UserPostComments


urlpatterns = [
    path('posts/', UserPost.as_view(), name='user_posts_gets'),
    path('posts/delete/<int:id>/', UserPostDelete.as_view(), name='user_posts_delete'),
    path('posts/<int:id>/', UserPostGet.as_view(), name='user_posts_post'),
    path('posts/comments/<int:id>/', UserPostComments.as_view(), name='user_posts_comments'),
    path('likes/<int:id>/', UserPostLikes.as_view(), name='user_posts_likes'),
    path('change/', UserProfilePost.as_view(), name='user-profile'),
    path('get/', UserProfileGet.as_view(), name='user-profile-get'),
]

