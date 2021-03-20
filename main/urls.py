from django.urls import path
from .views import CurrentFriends, Message, Reaction, Subscriptions, Requested


urlpatterns = [
    path('get-friends/', CurrentFriends.as_view(), name='current-friends'),
    path('get-requests/', Requested.as_view(), name='requested'),
    path('get-subscriptions/', Subscriptions.as_view(), name='subscription'),
    path('messages/', Message.as_view(), name='message'),
    path('manage-friends/', Reaction.as_view(), name='reaction'),
]