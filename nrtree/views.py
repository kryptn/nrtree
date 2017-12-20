from aiohttp.web import Request, json_response
from py2neo import Node, NodeSelector
from yarl import URL

from nrtree import Settings


def serialize_node(request: Request, node: Node):
    node_type = [l for l in node.labels() if l != 'Thing'][0]
    uri_path = request.app.router[node_type].url_for(id=node['id']).path
    url = URL.build(**Settings.yarl, path=uri_path)

    data = dict(node)
    data[f'{node_type.lower()}_url'] = str(url)
    return data


def select(request: Request, *args, **kwargs):
    selector = NodeSelector(request.app.graph)
    return selector.select(*args, **kwargs)


async def show_submissions(request: Request) -> json_response:
    nodes = [serialize_node(request, node) for node in select(request, 'Submission')]
    return json_response(nodes)


async def show_submission(request: Request) -> json_response:
    node = select(request, 'Submission', id=request.match_info['id']).first()
    return json_response(serialize_node(request, node))
