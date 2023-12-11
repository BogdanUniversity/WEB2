from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
babel = Babel(app)
admin = Admin(app,template_mode='bootstrap4')
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.app_context().push()
from app import views, models