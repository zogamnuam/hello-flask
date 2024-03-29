from flask import Flask , render_template, redirect,request,url_for,session, flash
from functools import wraps

app = Flask(__name__)

app.secret_key = "spider"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
	#return "Hello World"
	return render_template("index.html")

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")	

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin' :
			error = 'Invalid credentials, please try again later'
		else:
			session['logged_in'] = True
			flash('You were just Logged in!')
			return redirect(url_for('home'))
	return render_template('login.html',error=error)


@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You were just logout')
	return redirect(url_for('welcome'))


if __name__ == '__main__':
	app.run(debug=True)
