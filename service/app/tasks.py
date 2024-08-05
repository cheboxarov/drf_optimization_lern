from celery import shared_task


@shared_task
def asdasd():
    import time
    time.sleep(10)
    print("shared debug task")
