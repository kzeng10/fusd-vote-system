import webapp2
import os
import jinja2
import json
import time
import datetime
import re
import hmac
from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.dirname(__file__)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
								autoescape = True)

#handler for the jinja2 env. allows us to use templates! c/p this code all you want for other projects
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template,**kw))

#defining db
class Voter(db.Model):
	name = db.StringProperty(required = True)
	isVoting = db.BooleanProperty(required = True)

#following segment is for hashing user_id
SECRET = '***' 	#lol
pw = '***' 		#change this to actual password...(not really secure but w/e)
def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()

def check_pass(h):
	if h == hash_str(pw):
		return h

class AdminHandler(Handler):
	def get(self):
		password_hash = self.request.cookies.get('pwhash')
		if check_pass(password_hash):
			#following is not async...now how to do asigc
			voters = db.GqlQuery('SELECT * FROM Voter')
			yes = [voter.name for voter in voters if voter.isVoting]
			no = [voter.name for voter in voters if not voter.isVoting]
			self.render('admin.html', voters = [yes, no]) 		#let the ajaxing begin
		else:
			self.redirect('/login')
	def post(self):
		#clear database!
		db.delete(Voter.all())
		self.redirect('/admin')

class LoginHandler(Handler):
	def get(self):
		self.render('login.html')

	def post(self):
		password = self.request.get('password')
		if password == pw:
			#successful login, set cookie and redirect
			self.response.headers.add_header('Set-Cookie', 'pwhash=' + hash_str(password) + ';Path=/')
			self.redirect('/admin')
		else:
			#unsuccessful login
			self.render('login.html', error = "Invalid password")

class VoteHandler(Handler):
	def get(self):
		lastRequest = self.request.cookies.get('lastRequest')
		name = self.request.cookies.get('name')
		if name is None: name = ""
		if lastRequest:
			lastRequest = datetime.datetime.fromtimestamp(int(lastRequest)).strftime('%b %d, %Y at %I:%M %p')
		self.render('vote.html', lastRequest = lastRequest, name = name) #{{if lastRequest}} <p>Last submitted ____</p>

	def post(self):
		lastRequest = self.request.cookies.get('lastRequest')
		if lastRequest:
			lastRequest = datetime.datetime.fromtimestamp(int(lastRequest)).strftime('%b %d, %Y at %I:%M %p')
		name = self.request.get('name')
		choice = self.request.get('choice')
		if name == "":
			self.render('vote.html', lastRequest = lastRequest, response = 'Please enter a name.')
		elif choice == "":
			self.render('vote.html', lastRequest = lastRequest, name = name, response = 'Please select an option.')
		else:
			choice = str(choice) == 'Yes'
			voter = Voter(name = name, isVoting = choice)
			voter.put()
			lastRequest = datetime.datetime.fromtimestamp(int(time.time()) - 8*3600).strftime('%b %d, %Y at %I:%M %p')
			self.response.headers.add_header('Set-Cookie', 'lastRequest=' + str(int(time.time())) + ';Path=/')
			self.response.headers.add_header('Set-Cookie', 'name=' + str(name) + ';Path=/')
			self.render('vote.html', lastRequest = lastRequest, name = name, response = 'Successfully submitted.')

class JSONHandler(Handler):
	def get(self):
		#returns JSON of all db entries
		voters = db.GqlQuery('SELECT * FROM Voter')
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		# format as {"speak": ["person1", "person2"], "quiet": ["person3"]}
		# add in last modified if necessary?
		speak = [voter.name for voter in voters if voter.isVoting]
		quiet = [voter.name for voter in voters if not voter.isVoting]
		jsonOut = {"speak": speak, "quiet": quiet}
		self.write(json.dumps(jsonOut))
