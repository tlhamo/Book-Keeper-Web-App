from flask import render_template, redirect, url_for, session
from app import app, lman, datab
from models import User, Book, Author, RegisterForm, LoginForm, readers
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

@app.route('/')
def index():
	return render_template('home.html')

@lman.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	error = None
	if form.validate_on_submit():
		# security check (may not be needed)
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				session['logged_in']=True
				# render_template('dashboard.html', form=form)
				return redirect(url_for('dashboard', user=user))
		error = 'Invalid username or password.'
	return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		hash_password = generate_password_hash(form.password.data, method='sha256');
		# put data into database
		new_user = User(username=form.username.data, password=hash_password, email=form.email.data)
		datab.session.add(new_user)
		datab.session.commit()
		# redirect to login page
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/grocery/<string:id>/')
def grocery(id):
	return render_template('grocery.html', id=id)

@app.route('/dashboard')
@login_required
def dashboard():
	reads = list(datab.session.query(readers).filter(readers.c.user_id==flask_login.current_user.id))
	authors = list(datab.session.query(Author.name))
	data = []
	authorsdata = {}
	# for book in readers:
	for tup in reads:
		book = Book.query.get(tup[1])
		data.append(book)
	for tup in authors:
		if tup[0] in authorsdata:
			authorsdata[tup[0]] += 1
		else:
			authorsdata[tup[0]] = 1
	values = authorsdata.values()
	print("authorsdata"+ str(authorsdata.values()))
	return render_template('dashboard.html', data=data, authorsdata = authorsdata, values=values)
