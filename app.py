from flask import Flask, render_template, request, redirect, url_for, flash, session
from wtforms import Form, TextField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import IntegrityError
import os, string, re, random, hashlib

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique=True)
	first = db.Column(db.String(20))
	last = db.Column(db.String(20))
	password = db.Column(db.String(100))
	salt = db.Column(db.String(24))

	def __init__(self, email, first, last, password, salt):
		self.email = email
		self.first = first
		self.last = last
		self.password = password
		self.salt = salt

	def __repr__(self):
		return '[id {}, email {}, first {}, last {}, password {}, salt {}]'.format(self.id, self.email, self. first, self.last, self.password, self.salt)

class RegistrationForm(Form):
	email = TextField('Email:', validators=[validators.required(), validators.length(min=2, max=80)])
	first = TextField('First Name:', validators=[validators.required(), validators.length(min=2, max=20)])
	last = TextField('Last Name', validators=[validators.required(), validators.length(min=2, max=20)])
	pass1= TextField('Password', validators=[validators.required(), validators.length(min=8, max=16), validators.equal_to('pass2') ])
	pass2= TextField('Re-Type Password', validators=[validators.required()])


class LoginForm(Form):
	email = TextField('Email:', validators=[validators.required()])
	pass1 = TextField('Password', validators=[validators.required()])

@app.route("/", methods=['GET','POST'])
def login():
	if 'username' in session:
		#we are already logged in
		return render_template('index.html', users=User.query.all())
	else:
		# We are NOT logged in
		form = LoginForm(request.form)
		if request.method == 'POST':
			# Request is from login button
			if form.validate():
				# Gather the fields
				email = request.form['email']
				pass1 = request.form['pass1']
				# Find a user with matching email
				u = User.query.filter_by(email=email).first()
				if u is not None:
					# Use the same salt on the input password and compare
					# the input hashed input_pass+salt to the hashed pass
					salt = u.salt
					pass1 = pass1+salt
					pass1 = hashlib.md5(pass1).hexdigest()
					if pass1==u.password: # If the passwords are hashed the same
						# Then the passwords are (probably) the same
						flash('Success! Logged in')
						session['username']=email
						return redirect(url_for('login'))
			return render_template('login.html', form=form)
		else:
			return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	# Load the form from the web page, and clean the whitespaces
	form = RegistrationForm(request.form) # Create a RegistrationForm to run all of the validators
	if request.method == 'POST':			# If this is a post request (made by the submit button)
		email= clean_whitespaces(request.form['email'])
		first= clean_whitespaces(request.form['first'])
		last = clean_whitespaces(request.form['last'])
		pass1= clean_whitespaces(request.form['pass1'])
		pass2= clean_whitespaces(request.form['pass2'])
		if form.validate():					# If all of our fields have data, white spaces should be cleaned before checking length
			if pass1 != pass2:				# Ensure the passwords match
				flash('Error: Passwords must match.')
			else:
				try:
					# Encrypt password so it wont be stored in plain text
					salt = ''
					while (len (salt) + len(pass1)) < 32:
						salt = salt+random.choice(string.letters)
					pass1 = pass1[:32]
					pass1 = hash(pass1+salt)
					# Try to register the user
					u = User(email, first, last, pass1, salt)
					db.session.add(u)
					db.session.commit()
				except IntegrityError:	# If the data cannot be added due to uniqueness constraints on the email parameter
					flash('Error: A user with this Email already exists.')
				else:					# If we successfully added the User
					flash('Hello '+ first + ' ' + last+" xyou have been registered!")
		else:
			flash('Error: All fields are required.')
	return render_template('register.html', form=form)

def clean_whitespaces(temp):
	return re.sub('\s+', '', temp)

def hash(temp):
	return hashlib.md5(temp).hexdigest()
if __name__ == '__main__':
	app.run()

