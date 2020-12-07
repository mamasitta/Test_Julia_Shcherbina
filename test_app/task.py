from __future__ import absolute_import, unicode_literals

import csv
import os

from celery import shared_task, Celery

from tes_project import celery
app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])


@shared_task(name="creation_task")
def creation_task(file_path, data_to, delimiter, quotechar):
    csv.register_dialect('myDialect', delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC)
    with open(file_path, "w") as file:
        writer = csv.writer(file, "myDialect")
        writer.writerow(data_to)
    file.closed
    return file_path
