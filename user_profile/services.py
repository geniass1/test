from user.models import NewUser
from main.models import Friends
from django.db.models import Exists, OuterRef


def friend_request_status(username, friends, subscriptions, requested):
    if username in friends:
        return "friend"
    elif username in subscriptions:
        return "subscription"
    elif username in requested:
        return "requested"


def get_friends(user):
    friends = NewUser.objects.filter(
        Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
        Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user))
    ).distinct()
    return friends


def get_subscriptions(user):
    subscriptions = NewUser.objects.filter(
        ~Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
        Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user, pending=False))
    ).distinct()
    return subscriptions


def get_requested(user):
    requested = NewUser.objects.filter(
        ~Exists(Friends.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
        Exists(Friends.objects.filter(who__id=OuterRef('pk'), whom=user, pending=True))
    ).distinct()
    return requested
