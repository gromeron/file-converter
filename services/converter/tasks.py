from celery import Celery


app = Celery('tasks', broker= 'redis://35.239.105.189:6379/0')


@app.task
def converter_test():
    return{"message":"home ok fro converter"}