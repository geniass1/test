from django.db import models
from user.models import NewUser


class UserPosts(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(null=True, upload_to="images/")
    title = models.TextField(null=True)
    likes = models.IntegerField(default=0)


class UserProfile(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_profile')
    image = models.ForeignKey(UserPosts, on_delete=models.CASCADE,
                               related_name='user_avatar', null=True)
    status = models.TextField(null=True, blank=True)


class Comments(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(UserPosts, on_delete=models.CASCADE, related_name='post', null=True)
    comment = models.CharField(max_length=300)


class Likes(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(UserPosts, on_delete=models.CASCADE, related_name='post_likes', null=True)
    is_liked = models.BooleanField(default=False)
