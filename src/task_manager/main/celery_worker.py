import time

from celery import Celery

celery_app = Celery(
    __name__, broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)


@celery_app.task(name="create_task")
def create_task(n):
    print(f"running task {n}")
    time.sleep(5)
    print(f"task {n} is done.")
