import os.path

import yaml


class Settings:
    # reddit settings
    reddit_secret = 'reddit secret'
    reddit_id = 'reddit id'
    user_agent = ' the user agent v0.1'

    # app settings
    host = '0.0.0.0'
    port = 8080

    # neo4j settings
    neo4j = {
        'host': 'localhost',
        'password': 'neo4j_password_here'
    }

    # convenience dicts

    praw_auth = {'client_secret': reddit_secret,
                 'client_id': reddit_id,
                 'user_agent': user_agent}

    Web = {
        'host': host,
        'port': port
    }

    yarl = {
        'host': host,
        'port': port,
        'scheme': 'http'
    }


def try_get_yaml(filename):
    data = None
    if os.path.isfile(filename):
        with open(filename) as fd:
            data = yaml.load(fd)
    return data


config_paths = ['/data/env.yml', 'env.yml']

for path in config_paths:
    data = try_get_yaml(path)
    if not data:
        continue
    for key, value in data.items():
        setattr(Settings, key, value)
