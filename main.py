from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, \
    login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import shortuuid, uuid, sqlite3

app = Flask(__name__)

#Application Settings
app.config['SECRET_KEY'] = "42c78b0e-5dbc-4083-8794-b745930a1b71"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['TESTING'] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


db_users = SQLAlchemy(app)
db_posts = SQLAlchemy(app)
db_messages = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db_users.Model):
    userId = db_users.Column(db_users.Integer, primary_key=True)
    userName = db_users.Column(db_users.String(15), unique=True, nullable=False)
    eMail = db_users.Column(db_users.String(50), unique=True, nullable=False)
    password = db_users.Column(db_users.String(150), nullable=False)
    isModerator = db_users.Column(db_users.Boolean, nullable=False)

class Message(db_messages.Model):
    messageId = db_messages.Column(db_messages.Integer, primary_key=True)
    ownerId = db_messages.Column(db_messages.Integer, nullable=False)
    postId = db_messages.Column(db_messages.Integer, nullable=False)
    message = db_messages.Column(db_messages.String(500), nullable=False)

class Post(db_posts.Model):
    postId = db_posts.Column(db_posts.Integer, primary_key=True)
    ownerId = db_posts.Column(db_posts.Integer)
    header = db_posts.Column(db_posts.String(100), default="Konu Yok")
    body = db_posts.Column(db_posts.String(5000), nullable=False)
    openToComments = db_posts.Column(db_posts.Boolean)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# app.errorhandler accepts error codes if you want to use 
# your customized error pages for different type of errors.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Homepage
@app.get("/")
def index():
    return render_template("index.html")

#default post page
@app.get("/post/<int:post_id>")
def post(post_id):
    return render_template("post.html")

@app.get("/login")
def login():
    return "This is login page!"

@app.get("/settings")
@login_required
def setting():
    return current_user.userId

if __name__=='__main__':
    app.run("0.0.0.0", port=8000)