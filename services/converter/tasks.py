from celery import Celery


app = Celery('tasks', broker= 'redis://redis:6379/0')


@app.task
def converter_test():
    return{"message":"home ok fro converter"}