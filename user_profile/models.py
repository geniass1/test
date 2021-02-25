from django.db import models
from user.models import NewUser


class UserPosts(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(null=True, upload_to="images/")
    title = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    is_liked = models.BooleanField()


class UserProfile(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user')
    avatar = models.ImageField(null=True, upload_to="images/")
    likes = models.IntegerField(default=0)
    is_liked = models.BooleanField()
    status = models.TextField(null=True)


class Comments(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(UserPosts, on_delete=models.CASCADE, related_name='post', null=True)
    profile_image = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile_image', null=True)
    comment = models.CharField(max_length=300)
