from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = '76de173de227420f653cf3c10a713543'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://banco_spfc_6b3g_user:bKreKG4eaWRmp4CzMRF7nc4k5krLS5s1@dpg-cvac3jfnoe9s73f7519g-a.oregon-postgres.render.com/banco_spfc_6b3g'

database = SQLAlchemy(app)
criptografia = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'loginspfc'
login_manager.login_message = 'Por favor para continuar, faça Login.'
login_manager.login_message_category = 'alert-info'


from spfcproject import routes
