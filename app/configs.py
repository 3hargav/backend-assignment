from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://redis:6379/0",
        backend='db+mysql://root:root@mysql_db:3306/foo'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
