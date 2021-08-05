from .admin import messaging


def send_to_firebase_cloud_messaging(users, title, body, uri, id=None):
    tokens = []
    for user in users:
        for token in user.tokens.all():
            tokens.append(token.token)

    # See documentation on defining a message payload.
    if id is None:
        uri = f'{uri}/'
    else:
        uri = f'{uri}/{id}/'
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
        android=messaging.AndroidConfig(notification=messaging.AndroidNotification(channel_id="500")),
        data={
            "uri": uri
        },
    )

    try:
        response = messaging.send_multicast(message)
        print(response)
        # Response is a message ID string.
    except Exception as e:
        print('예외가 발생했습니다.', e)
