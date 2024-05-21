from celery import Celery

def make_celery(app):
    app.config['CELERY_BROKER_TRANSPORT_URL'] = 'redis://34.101.77.142:6379/0'
    app.config['RESULT_BACKEND'] = 'redis://34.101.77.142:6379/0'
    app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True 
    celery = Celery(app.name, backend=app.config['RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_TRANSPORT_URL'], include=['models.call_model']) 
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery