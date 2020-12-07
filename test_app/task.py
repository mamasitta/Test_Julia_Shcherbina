from __future__ import absolute_import, unicode_literals

import csv

from celery import shared_task


@shared_task(name="creation_task")
def creation_task(file_path, data_to, delimiter, quotechar):
    csv.register_dialect('myDialect', delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_NONNUMERIC)
    with open(file_path, "w") as file:
        writer = csv.writer(file, "myDialect")
        writer.writerow(data_to)
    file.closed
    return file_path



