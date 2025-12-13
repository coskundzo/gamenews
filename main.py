from flask import Flask, render_template
import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/features.html')
def features():
    return render_template('features.html')

@app.route('/pricing.html')
def pricing():
    return render_template('pricing.html')

@app.route('/faqs.html')
def faqs():
    return render_template('faqs.html')


# Login işlemi için hem GET hem POST destekleyen route
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    from flask import request, redirect, url_for, flash
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = session.query(users).filter(
            ((users.username == username) | (users.email == username)) & (users.password == password)
        ).first()
        if user:
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
from flask import request, redirect, url_for, flash

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not username or not email or not password:
        flash('Tüm alanları doldurun!', 'danger')
        return redirect(url_for('signup'))
    # Aynı kullanıcı adı veya email var mı kontrolü
    if session.query(users).filter((users.username == username) | (users.email == email)).first():
        flash('Kullanıcı adı veya email zaten kayıtlı!', 'danger')
        return redirect(url_for('signup'))
    new_user = users(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
