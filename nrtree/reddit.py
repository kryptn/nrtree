from typing import List, Iterable

import praw
from praw import models
from praw.models.comment_forest import MoreComments
from py2neo import Node, Relationship
from py2neo import Transaction, Graph

from nrtree import Settings
from nrtree.graph import (Comment, Submission, Subreddit, Redditor, ChildOf, AuthoredBy)

reddit = praw.Reddit(**Settings.praw_auth)


def top_ten(subreddit_name: str) -> Iterable[models.Submission]:
    return reddit.subreddit(subreddit_name).hot(limit=10)


def itercomments(comments: models.comment_forest) -> Iterable[models.Comment]:
    # turns a comment forest into a generator that expands MoreComments
    for comment in comments.list():
        if isinstance(comment, MoreComments):
            continue
        yield comment


def submission_graph(submission: models.Submission):
    # returns a list of nodes and relationships to create/merge from a submission
    nodes = [Submission(submission), Subreddit(submission.subreddit)]
    relationships = [ChildOf(*nodes)]

    print(f'Pulling thread {submission.subreddit.display_name_prefixed} "{submission.title}"')
    for comment in itercomments(submission.comments):

        cn = Comment(comment)
        nodes.append(cn)
        relationships.append(ChildOf(cn, Node(id=comment.parent().id)))

        if comment.author:
            rn = Redditor(comment.author)
            nodes.append(rn)
            relationships.append(AuthoredBy(cn, rn))

    return nodes, relationships


def merge_nodes_and_relationships(tx: Transaction, nodes: List[Node], relationships: List[Relationship]):
    for node in nodes:
        tx.merge(node)
    for rel in relationships:
        tx.merge(rel)


def top_10_and_insert(graph: Graph, subreddit_name: str):
    nodes = []
    relationships = []
    for sub in top_ten(subreddit_name):
        n, r = submission_graph(sub)
        nodes.extend(n)
        relationships.extend(r)

    with graph.begin() as tx:
        merge_nodes_and_relationships(tx, nodes, relationships)
