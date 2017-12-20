class Settings:
    reddit_secret = 'reddit secret'
    reddit_id = 'reddit id'
    user_agent=' the user agent v0.1'

    praw_auth = {'client_secret': reddit_secret,
                 'client_id': reddit_id,
                 'user_agent': user_agent}

    host = 'localhost'
    port = 9393

    Web = {
        'host': host,
        'port': port
    }

    yarl = {
        'host': host,
        'port': port,
        'scheme': 'http'
    }
