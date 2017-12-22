from celery import Celery

#name for list of tasks that follow (named tasks), broker is where messages stored (message queue)
# for different message queue there is different connection string, amqp for RabbitMQ
app = Celery('tasks', broker='amqp://localhost//')

@app.task
def reverse(string):
    return string[::-1]


""" Tell Celery what tasks want it to be available to execute:
$ celery -A tasks  worker --loglevel=info

"""