from datetime import timedelta
from flask import Flask

from .models import db, Videos, ApiKeys, Thumbnails
from .routes import main
from .configs import make_celery


def create_app():
    app = Flask(__name__)

    mysql_conn_str = "mysql://root:root@mysql_db:3306/foo"
    app.config["SQLALCHEMY_DATABASE_URI"] = mysql_conn_str

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.config['imports'] = ('app.tasks',)
    app.config['beat_schedule'] = {
        'async-fetch': {
            'task': 'app.tasks.fetch_youtube_videos',
            'schedule': timedelta(seconds=20)
        },
    }
    app.config['timezone'] = 'UTC'
    celery = make_celery(app)
    celery.set_default()

    app.register_blueprint(main)

    return app, celery
