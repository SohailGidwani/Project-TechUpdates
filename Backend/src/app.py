from flask import Flask
from flask_apscheduler import APScheduler
from api import api_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    return app, scheduler

app, scheduler = create_app()

if __name__ == '__main__':
    app.run(debug=True)
