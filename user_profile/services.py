def friend_request_status(username, friends, subscriptions, requested):
    # breakpoint()
    if username in list(map(lambda x: x['username'], friends)):
        return 'FRIEND'
    elif username in list(map(lambda x: x['username'], subscriptions)):
        return 'SUBSCRIBED'
    elif username in list(map(lambda x: x['username'], requested)):
        return 'REQUEST'
    return 'NO'
