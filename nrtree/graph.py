from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo, Label

from praw import models

DELETED = '[deleted]'
REMOVED = '[removed]'

class ChildOf(Relationship): pass
class AuthoredBy(Relationship): pass


class Thing(Node):
    def __init__(self, *labels, **properties):
        if 'Thing' not in labels:
            labels = (*labels, 'Thing')
        super().__init__(*labels, **properties)

class Comment(Thing):
    def __init__(self, comment):
        labels = ('Comment',)
        author = comment.author.name if comment.author else DELETED
        properties = {
            'id': comment.id,
            'author': author,
        }
        super().__init__(*labels, **properties)

class Submission(Thing):
    def __init__(self, submission):
        labels = ('Submission',)
        author = submission.author.name if submission.author else DELETED
        properties = {
            'id': submission.id,
            'author': author,
        }
        super().__init__(*labels, **properties)

class Redditor(Thing):
    def __init__(self, redditor):
        labels = ('Redditor',)
        properties = {
            'id': redditor.id,
            'name': redditor.name
        }
        super().__init__(*labels, **properties)








if __name__ == '__main__':
    graph = Graph()