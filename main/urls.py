from django.urls import path
from .views import CurrentFriends, Message, Reaction


urlpatterns = [
    path('current-friends/', CurrentFriends.as_view(), name='current-friends'),
    path('message/<int:id>/', Message.as_view(), name='message'),
    path('reaction/<int:id>/', Reaction.as_view(), name='reaction'),
]