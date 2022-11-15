from celery import Celery


app = Celery('tasks', broker= 'redis://35.222.185.225:6379/0')
#app = Celery('tasks', broker= 'redis://localhost:6379/0')


@app.task(name="convertion")
def converter_test():
    return{"message":"home ok from converter"}
