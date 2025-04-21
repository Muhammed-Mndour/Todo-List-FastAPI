import logging

from fastapi import FastAPI

from util import util

logger = logging.getLogger(__name__)


def create_app():
    app_params = {
        "title": f"To-Do List Public API",
        "description": f"To-Do List Public API",
        "version": "1.0.0",
        "docs_url": '/swagger',
        "redoc_url": '/docs',
    }

    app = FastAPI(**app_params)
    app.debug = not util.IS_PRODUCTION

    return app


app = create_app()
