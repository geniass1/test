def friend_request_status(username, friends, subscriptions, requested):
    # breakpoint()
    if username in list(map(lambda x: x['username'], friends)):
        return 'friend'
    elif username in list(map(lambda x: x['username'], subscriptions)):
        return 'subscribed'
    elif username in list(map(lambda x: x['username'], requested)):
        return 'request'
    return 'no'
