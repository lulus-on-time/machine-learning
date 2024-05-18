from celery import Celery

def make_celery(app):
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['BROKER_CONNECTION_RETRY_ON_STARTUP'] = True 
    celery = Celery(app.name, backend=app.config['RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'], include=['models.call_model']) 
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery