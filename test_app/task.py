from __future__ import absolute_import
from celery import shared_task
from test_project.celery import app


@app.task
def test(param):
    return 'The test task executed with argument "%s" ' % param