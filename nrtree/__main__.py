import click
from IPython import embed
from aiohttp import web

from nrtree import Settings
from nrtree.app import make_app
from nrtree.graph import make_graph_with_creds


@click.group()
def cli():
    pass


@click.command()
def runserver():
    app = make_app()
    web.run_app(app, **Settings.Web)


@click.command()
def shell():
    graph = make_graph_with_creds()
    embed()


cli.add_command(shell)
cli.add_command(runserver)

if __name__ == '__main__':
    cli()
