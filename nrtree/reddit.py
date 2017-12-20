import praw
from functools import partial
from praw.models.comment_forest import MoreComments
from py2neo import Graph, Node, Relationship
from py2neo.ogm import RelatedTo
from nrtree import Settings
from nrtree.graph import Comment, Submission, Redditor, ChildOf, AuthoredBy

reddit = praw.Reddit(**Settings.praw_auth)

def top_ten(subreddit_name):
    return reddit.subreddit(subreddit_name).hot(limit=10)

def itercomments(comments):
    for comment in comments.list():
        if isinstance(comment, MoreComments):
            continue
        yield comment

def insert_submission(submission, graph):
    relationships = []
    things = {}
    sn = Submission(submission)
    things[sn['id']] = sn

    print(f'Pulling thread "{submission.title}"')

    for comment in itercomments(submission.comments):
        cn = Comment(comment)
        things[cn['id']] = cn
        relationships.append(ChildOf(cn, Node(id=comment.parent().id)))

        if comment.author:
            an = Redditor(comment.author)
            things[an['id']] = an
            relationships.append(AuthoredBy(cn, an))


    with graph.begin() as tx:
        for thing in things.values():
            tx.merge(thing)
        for rel in relationships:
            tx.merge(rel)



def dump_all(graph):
    graph.run("match (n) detach delete n")
    graph.run("create index on :Thing(id)")


if __name__ == '__main__':
    graph = Graph()