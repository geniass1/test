from django.urls import path
from .views import CurrentFriends, Message, Reaction, Subscriptions


urlpatterns = [
    path('current-friends/<int:id>/', CurrentFriends.as_view(), name='current-friends'),
    path('subscription/<int:id>/', Subscriptions.as_view(), name='subscription'),
    path('message/<int:id>/', Message.as_view(), name='message'),
    path('add-to-friends/', Reaction.as_view(), name='reaction'),
]