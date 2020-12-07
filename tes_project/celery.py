import csv
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from django.shortcuts import redirect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_project.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('tes_project', backend='redis', broker='redis://localhost:6379')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task_test(self, param):
    return 'The test task executed with argument "%s" ' % param


@app.task(bin=True)
def creation_task(file_path, data_to, dialect):
    dialect = dialect
    with open(file_path, "w") as file:
        writer = csv.writer(file, dialect=dialect)
        writer.writerow(data_to)
    file.closed
    # new_file_obj = CsvStorage(user_create_id=user_id, file_name=schema_name, file_path=file_path)
    # new_file_obj.save()
    return redirect("index")
