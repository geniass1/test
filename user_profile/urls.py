from django.urls import path

from .views import UserPost, UserPostLikes, UserProfilePost, UserProfileMyGet, \
    UserPostComments, UserProfileGet

urlpatterns = [
    path('posts/', UserPost.as_view(), name='user_posts_gets'),
    path('posts/delete/<int:id>/', UserPost.as_view(), name='user_posts_delete'),
    path('posts/<int:id>/', UserPost.as_view(), name='user_posts_post'),
    path('posts/comments/<int:id>/', UserPostComments.as_view(), name='user_posts_comments'),
    path('likes/<int:id>/', UserPostLikes.as_view(), name='user_posts_likes'),
    path('change/', UserProfilePost.as_view(), name='user-profile-change'),
    path('my/', UserProfileMyGet.as_view(), name='user-profile-my'),
    path('<int:id>/', UserProfileGet.as_view(), name='user-profile-get'),
]
