from flask import Flask,session, flash,render_template,redirect,request,url_for
from functools import wraps
import sqlite3

app=Flask(__name__)
app.secret_key='secret_key'
app.database='sample.db'


def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

def connect_db():
	return sqlite3.connect(app.database)

@app.route('/')
@login_required
def home():
	g=connect_db()
	cur=g.execute('select * from posts')
	posts=[]
	for row in cur.fetchall():
		posts.append(dict(title=row[0],description=row[1]))
	#print posts
	
	#posts=[dict(title=row[0],description=row[1]) for row in cur.fetchall()]
	
	g.close()	
	return render_template('index.html',posts=posts)


@app.route('/welcome')
def welcome():
	
	return render_template('welcome.html')

@app.route('/login', methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error='Invalid credendtials. Please try it again.'
		else:
			session['logged_in']=True
			flash('You were just logged in')
			return redirect(url_for('home'))
	return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You were just logged out!')
	return redirect(url_for('welcome'))



if __name__=="__main__":
	app.run(debug=True)