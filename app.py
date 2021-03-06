from datetime import datetime
from flask import Flask, request, render_template_string, render_template
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin, user_logged_out
from sqlalchemy.sql import table, column, select 
from sqlalchemy import MetaData

""" Flask application factory """
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///basic_app.sqlite'
app.config["SECRET_KEY"] = 'This is an INSECURE secret!! DO NOT use this in production!!'
app.config["USER_ENABLE_EMAIL"] = False

babel = Babel(app)
@babel.localeselector

def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]

db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer(), primary_key=True)
    word = db.Column(db.String(50), unique=True)
    word_tr = db.Column(db.String(50), unique=True)
    
user_manager = UserManager(app, db, User)
db.create_all()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/add_word')
def add_word():
      return render_template('add_word.html')

@app.route('/word_insert', methods = ['POST', 'GET'])
def word_insert():
    if request.method == 'POST':
        try:
            wordtr = request.form['wordTR']
            worden = request.form['wordEN']
            
            if(Word.query.filter_by(word = worden).first()):
                msg = "Eklemeye çalıştığın kelime havuzda mevcut! Yeni kelimelerini bekliyoruz :)"
            else:
                insert = Word(word = worden, word_tr = wordtr)
                db.session.add(insert)
                db.session.commit()
                msg = "Kelimelik havuzuna yeni bir kelime kazandırdın, teşekkürler!" 
        except:
            msg = "Kelimelik hazvuzuna yeni bir kelime kazandırırken bir hata oluştu, tekrar dene!"
        finally:
            return render_template("message.html", message = msg)

@app.route('/word_pool')
def word_pool():
    row = Word.query.order_by(Word.id).all()
    return render_template('word_pool.html', rows = row)     
#@user_logged_out.connect_via(app)
#def _after_login_hook(sender, user, **extra):
#logout olduktan sonra

if __name__ == '__main__':
    app.run(threaded=True, port=5000)