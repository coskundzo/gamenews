from flask import Flask, render_template, session as flask_session, request, redirect, url_for, flash
import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()

app = Flask(__name__)
app.secret_key = 'supersecretkey_1234567890'  # Güvenli bir secret key belirleyin

class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

# users tablosunu oluştur
Base.metadata.create_all(engine)

@app.route('/')
@app.route('/index.html')
def home():
    username = flask_session.get('username')
    return render_template('index.html', username=username)

@app.route('/about.html')
def about():
    username = flask_session.get('username')
    return render_template('about.html', username=username)

@app.route('/features.html')
def features():
    username = flask_session.get('username')
    return render_template('features.html', username=username)

@app.route('/pricing.html')
def pricing():
    username = flask_session.get('username')
    return render_template('pricing.html', username=username)

@app.route('/faqs.html')
def faqs():
    username = flask_session.get('username')
    return render_template('faqs.html', username=username)

@app.route('/live.html')
def live():
    username = flask_session.get('username')
    if not username:
        flash('Canlı yayını izlemek için giriş yapmalısınız!', 'warning')
        return redirect(url_for('login'))
    return render_template('live.html', username=username)


# Login işlemi için hem GET hem POST destekleyen route
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db_session.query(users).filter(
            ((users.username == username) | (users.email == username)) & (users.password == password)
        ).first()
        if user:
            flask_session['username'] = user.username
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Kullanıcı adı/email veya şifre hatalı!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')


# Kullanıcı ekleme route'u
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not username or not email or not password:
        flash('Tüm alanları doldurun!', 'danger')
        return redirect(url_for('signup'))
    # Aynı kullanıcı adı veya email var mı kontrolü
    if db_session.query(users).filter((users.username == username) | (users.email == email)).first():
        flash('Kullanıcı adı veya email zaten kayıtlı!', 'danger')
        return redirect(url_for('signup'))
    new_user = users(username=username, email=email, password=password)
    db_session.add(new_user)
    db_session.commit()
    flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
    return redirect(url_for('login'))

# Logout route'u
@app.route('/logout')
def logout():
    flask_session.pop('username', None)
    flash('Çıkış yapıldı!', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
