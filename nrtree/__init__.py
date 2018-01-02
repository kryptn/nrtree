class Settings:
    reddit_secret = 'reddit secret'
    reddit_id = 'reddit id'
    user_agent=' the user agent v0.1'

    praw_auth = {'client_secret': reddit_secret,
                 'client_id': reddit_id,
                 'user_agent': user_agent}

    # app settings
    host = '0.0.0.0'
    port = 8080

    Web = {
        'host': host,
        'port': port
    }

    # convenience payload for yarl
    yarl = {
        'host': host,
        'port': port,
        'scheme': 'http'
    }

    # neo4j settings
    neo4j = {
        'host': 'localhost',
        'password': 'neo4j_password_here'
    }
