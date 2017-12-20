import praw
from praw.models.comment_forest import MoreComments
from py2neo import Node

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


def submission_graph(submission):
    nodes = []
    relationships = []

    sn = Submission(submission)
    nodes.append(sn)

    print(f'Pulling thread "{submission.title}"')
    for comment in itercomments(submission.comments):
        cn = Comment(comment)
        nodes.append(cn)
        relationships.append(ChildOf(cn, Node(id=comment.parent().id)))

        if comment.author:
            an = Redditor(comment.author)
            relationships.append(AuthoredBy(cn, an))

    return nodes, relationships


def merge_nodes_and_relationships(tx, nodes, relationships):
    for node in nodes:
        tx.merge(node)
    for rel in relationships:
        tx.merge(rel)


def top_10_and_insert(graph, subreddit_name):
    nodes = []
    relationships = []
    for sub in top_ten(subreddit_name):
        n, r = submission_graph(sub)
        nodes.extend(n)
        relationships.extend(r)

    with graph.begin() as tx:
        merge_nodes_and_relationships(tx, nodes, relationships)
