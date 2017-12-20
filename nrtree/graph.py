from praw import models
from py2neo import Node, Relationship, Graph

DELETED = '[deleted]'
REMOVED = '[removed]'


class ChildOf(Relationship): pass


class AuthoredBy(Relationship): pass


class Thing(Node):
    def __init__(self, *labels, **properties):
        if 'Thing' not in labels:
            labels = (*labels, 'Thing')
        obj = properties.pop('__obj', None)
        if obj:
            properties['id'] = obj.id
            properties['permalink'] = getattr(obj, 'permalink', None)
            properties['created_utc'] = obj.created_utc
        super().__init__(*labels, **properties)


class Comment(Thing):
    def __init__(self, comment: models.Comment):
        labels = ('Comment',)
        author = comment.author.name if comment.author else DELETED
        properties = {
            '__obj': comment,
            'id': comment.id,
            'author': author,
        }
        super().__init__(*labels, **properties)


class Submission(Thing):
    def __init__(self, submission: models.Submission):
        labels = ('Submission',)
        author = submission.author.name if submission.author else DELETED
        properties = {
            '__obj': submission,
            'id': submission.id,
            'author': author,
        }
        super().__init__(*labels, **properties)


class Subreddit(Thing):
    def __init__(self, subreddit: models.Subreddit):
        labels = ('Subreddit',)
        properties = {
            '__obj': subreddit,
            'id': subreddit.fullname,
            'name': subreddit.display_name_prefixed
        }
        super().__init__(*labels, **properties)


class Redditor(Thing):
    def __init__(self, redditor: models.Redditor):
        labels = ('Redditor',)
        properties = {
            '__obj': redditor,
            'id': redditor.id,
            'name': redditor.name
        }
        super().__init__(*labels, **properties)


def dump_all(graph):
    graph.run('match (n) detach delete n')
    graph.run('create index on :Thing(id)')


async def init_graph(app):
    app.graph = Graph()
