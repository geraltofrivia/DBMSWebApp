from bottle import route, run, get, post, request
import db

database = db.Datastore()

html = '''
<body> 
	<form method = 'post'>
		<br>
		<label> <h2> Register. </h2> <hr> <br> Enter your details below </label> <br>
		<label> Name </label> <input type="text" name="username"> </label> <br>
		<label> Password </label> <input type="password" name="password"> </label> <br>
		<label> Retype Password </label> <input type="password" name="password_r"> </label> <br>
		<input type="submit">
	</form>
</body> '''
		

@route('/register')
def hello():
	return html


@route('/register', method='POST')
def echo():
	username = request.forms.get('username')
	password = request.forms.get('password')
	password_r = request.forms.get('password_r')

	if database.is_existing_user:
		print username, password

run(host='localhost', port=8080, debug=True)
