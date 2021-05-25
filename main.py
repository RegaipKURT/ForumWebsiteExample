from flask import Flask, render_template, __version__, \
    url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, \
    login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import shortuuid, uuid, sqlite3


app = Flask(__name__)

app.config['SECRET_KEY'] = "42c78b0e-5dbc-4083-8794-b745930a1b71"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['TESTING'] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

@app.get('/')
def index():
    return "Initialization Completed Succesfully!"

if __name__=='__main__':
    app.run("0.0.0.0", port=8000)