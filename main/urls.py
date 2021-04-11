from django.urls import path
from .views import CurrentFriends, Message, Reaction, Subscriptions, Requested, ManageSubscriptions


urlpatterns = [
    path('get-friends/<int:id>/', CurrentFriends.as_view(), name='current-friends'),
    path('get-requests/<int:id>/', Requested.as_view(), name='requested'),
    path('get-subscriptions/<int:id>/', Subscriptions.as_view(), name='subscription'),
    path('manage-subscriptions/', ManageSubscriptions.as_view(), name='manage-subscription'),
    path('messages/', Message.as_view(), name='message'),
    path('manage-friends/', Reaction.as_view(), name='reaction'),
]