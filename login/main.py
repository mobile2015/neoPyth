from flask import Flask, render_template, request, flash, redirect, url_for
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, flash, current_user, logout_user
from py2neo import Graph, Node
from email.mime.text import MIMEText
import uuid
import hashlib
import random
import string
import smtplib


app = Flask(__name__)  
app.secret_key = 'mobilne_2015'   
login_manager = LoginManager()
login_manager.init_app(app)
graph = Graph()
#graph.delete_all()	


class User(UserMixin):

	def __init__(self,_first_name,_last_name,_email,_login,_password,_group="None",_active=0):
		self.first_name = _first_name
		self.last_name = _last_name
		self.email = _email
		self.login = _login
		self.password = _password
		self.active = _active
		self.group = _group
		
	def __init__(self,record):
		self.first_name = record["first_name"]
		self.last_name = record["last_name"]
		self.email = record["email"]
		self.login = record["login"]
		self.password = record["password"]
		if record["group"]=="None":
			self.group = None
		if record["active"]==1:
			self.active = True
		else:
			self.active = False
			
	def set_group(self,_group):
		self.group = _group

	def is_active(self):
		return self.active
		
	def get_id(self):
		return self.login

	def is_anonymous(self):
		return False

		
@app.route('/')
def home():
	return render_template('home.html')
	
	
@login_manager.user_loader
def load_user(_login):
	query = 'MATCH (node:User) WHERE node.login = "' + _login + '" RETURN node'
	for tmp in graph.cypher.execute(query):
		return User(tmp[0])
	return None

	
@app.route('/sign_up',methods=['GET','POST'])
def sign_up():
	if current_user.is_anonymous():
		if request.method == 'GET':
			return render_template('sign_up.html')
		else:
			_activation_code = random_string(16)
			_first_name = request.form['fname']
			_last_name = request.form['lname']
			_email = request.form['email']
			_login = request.form['login']
			_password = hash_password(request.form['password'])
			_user = Node("User",first_name=_first_name,
				last_name=_last_name,
				email=_email,
				login=_login,
				password=_password,
				_group="None",
				active=0,
				activation_code=_activation_code)
			graph.create(_user)
			_mail_content = "localhost:5000"+url_for('activate_user')+'?login='+_login+'&code='+_activation_code
			send_activation_code(_email,_mail_content)
			flash("Check your email for activation link. If you are too lazy or used fake e-mail just use this link:   "+"localhost:5000"+url_for('activate_user')+'?login='+_login+'&code='+_activation_code)
	else:
		flash("Cant create new account while logged in?")
	return redirect(url_for('home'))


@app.route('/activate_user',methods=['GET','POST'])
def activate_user():
	login = request.args.get('login')
	code = request.args.get('code')
	query = 'MATCH (node:User) WHERE node.login = "' + login + '" RETURN node'
	for tmp in graph.cypher.execute(query):
		if tmp[0]["active"]==1:
			flash(login + "your account has already been activated.")
		elif tmp[0]["activation_code"]==code:
			query = 'MATCH (node:User) where node.login="' + login + '" set node.active=' + str(1)
			graph.cypher.execute(query)
			query = 'MATCH (node:User) where node.login="' + login + '" remove node.activation_code'
			graph.cypher.execute(query)
			flash("Congrats "+login+" You have just activated your account.")
		else:
			flash("Incomplete or incorrect data!")
	return redirect(url_for('home'))

	
@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
	if request.method == 'GET':
		return render_template('sign_in.html')
	else:
		_login = request.form['login']
		_password = request.form['password']
		query = 'MATCH (node:User) WHERE node.login = "' + _login + '" RETURN node'
		cnt=0
		for tmp in graph.cypher.execute(query):
			if check_password(tmp[0]["password"],_password):
				if tmp[0]["active"]==1:
					login_user(User(tmp[0]))
					flash("Welcome "+_login+". You are logged in!")
				else:
					_mail_content = "localhost:5000"+url_for('activate_user')+'?login='+_login+'&code='+tmp[0]["activation_code"]
					send_activation_code(tmp[0]["email"],_mail_content)
					flash("Check your email for activation link. If you are too lazy or used fake e-mail just use this link:   "+_mail_content)
				cnt=cnt+1				
				break
			else:
				flash("Incorrect (incomplete) login or password")
		if cnt==0:
			flash("Incorrect user login")
		return redirect(url_for('home'))

		
@app.route('/cypher',methods=['GET','POST'])
@login_required
def cypher():
	if request.method == 'GET':
		return render_template('query.html')
	else:
		_query = request.form['query']
		if _query:
			result = graph.cypher.execute(_query)
			s = ""
			if result:
				for res in result:
					s = s + str(res[0]) + "\n";
				flash(s)
		else:
			flash("No query to execute")
		return redirect(url_for('cypher'))
	
	
@app.route('/sign_out',methods=['GET','POST'])
@login_required
def sign_out():
	flash("User "+current_user.login+" logged out!")
	logout_user()
	return redirect(url_for('home'))

	
def random_string(_length):
	return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for i in range(_length))

	
def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    	
	
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()	


def send_activation_code(_mail,_link):
	pass
	'''msg = MIMEText("To activate your account just use this link:   "+_link)
	msg['Subject'] = 'Mobilne 2015 Activation Code'
	msg['From'] = "mobilne2015_neo4j_python_project@agh.edu.pl"
	msg['To'] = _mail

	s = smtplib.SMTP('localhost')
	s.sendmail("mobilne2015_neo4j_python_project@agh.edu.pl", _mail, msg.as_string())
	s.quit()'''
	
if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')
