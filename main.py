from bottle import route, run, get, post, request
from bottle import jinja2_view, route
import db

database = db.Datastore()

@route('/register')
@jinja2_view('register.html')
def hello():
	return 


@route('/register', method='POST')
def echo():
	username = request.forms.get('username')
	password = request.forms.get('password')
	password_r = request.forms.get('password_r')

	if database.is_existing_user:
		print username, password

run(host='localhost', port=8080, debug=True)

@route('/users')
def users():
	users = database.get_all_users()


