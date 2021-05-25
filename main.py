from flask import Flask, render_template, url_for, \
    redirect, request
from flask.helpers import send_from_directory
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, \
    login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import re, datetime, shortuuid, uuid, sqlite3

app = Flask(__name__)

#Application Settings
app.config['SECRET_KEY'] = "42c78b0e-5dbc-4083-8794-b745930a1b71"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
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
    id = db_users.Column(db_users.Integer, primary_key=True)
    userName = db_users.Column(db_users.String(500), unique=True, nullable=False)
    eMail = db_users.Column(db_users.String(500), unique=True, nullable=False)
    password = db_users.Column(db_users.String(500), nullable=False)
    isModerator = db_users.Column(db_users.Boolean, nullable=False)

class Message(db_messages.Model):
    id = db_messages.Column(db_messages.Integer, primary_key=True)
    ownerID = db_messages.Column(db_messages.Integer, nullable=False)
    postID = db_messages.Column(db_messages.Integer, nullable=False)
    message = db_messages.Column(db_messages.String(500), nullable=False)
    messageDate = db_messages.Column(db_messages.DateTime)

class Post(db_posts.Model):
    id = db_posts.Column(db_posts.Integer, primary_key=True)
    ownerID = db_posts.Column(db_posts.Integer)
    header = db_posts.Column(db_posts.String(100), default="Konu Yok")
    body = db_posts.Column(db_posts.String(5000), nullable=False)
    openToComments = db_posts.Column(db_posts.Boolean)
    postDate = db_posts.Column(db_posts.DateTime)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    if current_user.is_authenticated:
        return render_template("/profile.html")
    else:
        return render_template("login.html")

@app.post('/login')
def loginUser():
    try:
        if request.method == "POST":
            email = re.sub(' +', ' ', str(request.form['email']).strip())
            password = str(request.form['password'])
            user = User.query.filter_by(eMail=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect("/")
                else:
                    return render_template("login.html", warn="Yanlış Bir Kullanıcı Adı veya Şifre Girdiniz!")
            else:
                return render_template("login.html", warn="Yanlış Bir Kullanıcı Adı veya Şifre Girdiniz!")
    except:
        return render_template("unknownError.html"), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.get("/signup")
def signup():
    return render_template("signup.html")

@app.post('/signup')
def signupUser():
    try:
        if request.method == "POST":
            email = re.sub(' +', ' ', str(request.form['email']).strip())
            password = str(request.form['password'])
            username = re.sub(' +', ' ', str(request.form['username']).strip())
            isModerator = 0
            
            uyari = '''Lütfen Girdiğiniz Değerleri kontrol ediniz! \nŞifre en az 8 karakter olmalı ve diğer değerler de uygun şekilde girilmiş olmalıdır!'''
            
            if username == "" or username == " " or password == "" or password == " " or len(password) < 8:
                return render_template("signup.html", warn=uyari)
            
            #I used pbkdf2 hash algorithm to be accordence with NIST
            hashed_password = generate_password_hash(password, method='pbkdf2:sha512:80000')
            new_user = User(userName=username, eMail=email, password=hashed_password, isModerator=isModerator)
            db_users.session.add(new_user)
            db_users.session.commit()
            
            print(hashed_password, username, password, email)
            return render_template("signup.html", warn="Kullanıcı eklendi.\nGiriş yapmak için giriş sayfasını kullanın.\n")
    
    except IntegrityError: #kullanıcı varsa dönecek hata
            return render_template("signup.html", warn="Kullanıcı adı veya E-mail sistemde zaten kayıtlı!")
    
    #if any other error occurs we will return unknownError page
    #according to errors we can show appropriate types of error.
    except:
        return render_template("unknownError.html"), 500


#user's settings page
@app.get("/settings")
@login_required
def setting():
    return current_user.userId

@app.get("/about")
def about():
    return render_template("about.html")

#user profile page defined with username
@app.get("/profile/<string:username>")
@login_required
def profilePage(username):
    try:
        return render_template(f"profile/{username}.html")
    except:
        return render_template("unknownError.html"), 500

#New topic page
@app.get("/addTopic")
@login_required
def addTopic():
    date = datetime.datetime.now()
    date = date.strftime("'%b %d, %Y'")
    return render_template("addTopic.html", date=date)

@app.post("/addTopic")
@login_required
def addTopicToPosts():
    if request.method == "POST":
        header = request.form["header"]
        content = request.form["content"]
        openToComments = 1 if request.form["openToComments"] == "Yorumlara Açık" else 0
        ownerID = current_user.id
        date = datetime.datetime.now()
        
        print(header, content, openToComments, ownerID, date)
        newPost = Post(header=header, body=content, openToComments=openToComments, ownerID=ownerID, postDate=date)
        db_posts.session.add(newPost)
        db_posts.session.commit()
        return render_template("index.html")
    else:
        return render_template("unknownError.html")
# I used default disallow.
# Because i don't want search engines to index my page.
@app.get("/robots.txt")
def robots():
    return send_from_directory("static", path="/static", filename="robots.txt")

if __name__=='__main__':
    app.run("0.0.0.0", port=8000)