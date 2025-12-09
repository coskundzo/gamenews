from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
