from aiohttp import web

from nrtree.graph import init_graph
from nrtree.routes import setup_routes


def make_app() -> web.Application:
    app = web.Application()

    app.on_startup.append(init_graph)

    setup_routes(app)

    return app
