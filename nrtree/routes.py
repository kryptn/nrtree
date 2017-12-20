from aiohttp import web

from nrtree.views import show_submissions, show_submission


def setup_routes(app: web.Application):
    app.router.add_get('/submissions/', show_submissions)
    app.router.add_get('/submissions/{id}/', show_submission, name='Submission')
