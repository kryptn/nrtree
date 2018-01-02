import platform

from aiohttp import web
from aiohttp.web import json_response
from py2neo import NodeSelector, Relationship, Node
from yarl import URL

from nrtree import Settings


class ThingView(web.View):
    thing_type = None
    relationship = None

    @property
    def graph(self):
        return self.request.app.graph

    def serialize_node(self, node):
        node_type = [l for l in node.labels() if l != 'Thing'][0]
        uri_path = self.request.app.router[node_type].url_for(id=node['id']).path
        url = URL.build(**Settings.yarl, path=uri_path)
        url_key = f'{node_type.lower()}_url'
        data = dict(node)
        data[url_key] = str(url)
        return data

    def selector(self, *args, **kwargs):
        _selector = NodeSelector(self.graph)
        nodes = _selector.select(*args, **kwargs)
        return [self.serialize_node(node) for node in nodes]

    def get_thing(self, thing_id):
        return self.selector(self.thing_type, id=thing_id)

    def get_tree(self, thing_id, depth=None):
        depth = f'..{depth}' if depth else ''
        subtree = f"""
        match (p:{self.thing_type} {{id:'{thing_id}'}})<-[:CHILD_OF*{depth}]-(c)
        with collect(p)+collect(c) as nodes
        match r=()<-[:CHILD_OF]-() return r
        """
        branches = self.graph.run(subtree).data()
        flat_data = {x for y in branches for x in y['n'].nodes()}
        tree = {n: self.serialize_node(n) for n in list(flat_data)}

        for branch in branches:
            nodes = branch['n'].nodes()
            for parent, child in zip(nodes, nodes[1:]):
                print(parent)
                if 'children' not in tree[parent]:
                    tree[parent]['children'] = []
                tree[parent]['children'].append(tree[child])

        root = [node for node in list(flat_data) if node['id'] == thing_id][0]
        return tree[root]

    async def get(self):
        flat = self.request.query.get('flat', None)
        thing_id = self.request.match_info.get('id', None)

        # if not flat:
        #    return json_response(self.get_tree(thing_id))

        if thing_id:
            return json_response(self.selector(self.thing_type, id=thing_id))
        return json_response(self.selector(self.thing_type))


class SubmissionView(ThingView):
    thing_type = 'Submission'


class CommentView(ThingView):
    thing_type = 'Comment'
    relationship = Relationship(Node(), 'CHILD_OF', Node())


class RedditorView(ThingView):
    thing_type = 'Redditor'


class SubredditView(ThingView):
    thing_type = 'Subreddit'


async def health(request: web.Request) -> web.Response:
    count = request.app.graph.run("match (n:Thing) return count(n) as node_count").data()
    check = {'healthy': True, 'node': platform.node()}
    check.update(count)
    return json_response(check)
