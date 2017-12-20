import click
from IPython import embed
from aiohttp import web

from nrtree.app import make_app
from nrtree.reddit import *


@click.group()
def cli():
    pass


@click.command()
def runserver():
    app = make_app()
    web.run_app(app, **Settings.Web)
    pass


@click.command()
def shell():
    graph = Graph()
    embed()


cli.add_command(shell)
cli.add_command(runserver)

if __name__ == '__main__':
    cli()
