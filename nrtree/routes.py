from aiohttp import web

# from nrtree.views import get_submission, get_submissions, get_redditor, get_comment
from nrtree.views import CommentView, RedditorView, SubmissionView, SubredditView, health


def setup_routes(app: web.Application):
    app.router.add_route('*', '/submission/{id}/', SubmissionView, name='Submission')
    app.router.add_route('*', '/submission/', SubmissionView, name='Submissions')
    app.router.add_route('*', '/subreddit/{id}/', SubredditView, name='Subreddit')
    app.router.add_route('*', '/subreddit/', SubredditView, name='Subreddits')
    app.router.add_route('*', '/redditor/{id}/', RedditorView, name='Redditor')
    app.router.add_route('*', '/redditor/', RedditorView, name='Redditors')
    app.router.add_route('*', '/comment/{id}/', CommentView, name='Comment')
    app.router.add_route('*', '/comment/', CommentView, name='Comments')
    app.router.add_route('*', '/health/', health, name='health')
