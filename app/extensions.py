from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()