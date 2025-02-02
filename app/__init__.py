from flask import Flask, render_template
from app.config import Development
from app.extensions import db, bootstrap, migrate
from app.models import Customer, Reservation, Table


def create_app():

    app = Flask(__name__)
    app.config.from_object(Development)
    
    #extensions init
    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)


    @app.route("/")
    def index():

        return render_template("index.html")

    with app.app_context():
        #register bp with the routes
        from app.routes import api
        app.register_blueprint(api, url_prefix="/api")

    return app