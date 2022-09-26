from __future__ import absolute_import, unicode_literals
from celery.decorators import task


from celery import shared_task

@shared_task
def add(x,y):
    return x+y



# @task(name='transfer_to_ready')
