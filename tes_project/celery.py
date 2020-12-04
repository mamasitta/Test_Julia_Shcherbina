import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tes_project.settings')

app = Celery('tes_project', backend='redis', broker='redis://localhost:6379')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task_test(self, param):
    return 'The test task executed with argument "%s" ' % param

