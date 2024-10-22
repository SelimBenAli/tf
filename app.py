from flask import Flask
from flask_cors import CORS

import pymysql

from personne import personne_bp
from tescaForms import forms_bp
from auth import auth_bp
from dashboard import dashboard_bp

app = Flask(__name__)
CORS(app)
app.secret_key = 'secret_key'

app.register_blueprint(personne_bp, url_prefix='/personne')
app.register_blueprint(forms_bp, url_prefix='/forms')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')


if __name__ == '__main__':
    app.run()
