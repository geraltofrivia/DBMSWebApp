from bottle import route, run, get, post, request
from bottle import jinja2_view, route
import psycopg2

database = psycopg2.connect(database='201201217', user='201201217', password='201201217',host='10.100.71.21', port='5432')
cur = database.cursor()

#HTML!
html_users = '''
<html>
  <head>
    <title></title>
    <meta content="">
    <style></style>
  </head>
	<body>
        <h2> Users </h2> <br> <hr>
        <ul>
            %s
        </ul> 
	</body> 
</html>
'''

html_login = '''
<html>
  <head>
    <title></title>
    <meta content="">
    <style></style>
  </head>
  <body>
    <h2> Login </h2> <br> <hr>
    <form method = "post">
        <br>
        <label> Name </label> <input type="text" name="username"> </label> <br>
        <label> Password </label> <input type="password" name="password"> </label> <br>
        <input type="submit">
    </form>
  </body>
</html>
'''

@route('/register')
@jinja2_view('register.html')
def register():
    return 

@route('/register', method='POST')
def register_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    password_r = request.forms.get('password_r')

@route('/users')
def print_users():
    cur.execute("SELECT * FROM lab5.user_acc;")
    l_users = cur.fetchall()
    usernames = ''
    for user in l_users:
        usernames += '<li>' + user[0]
    result = html_users % usernames
    return result

@route('/login')
def login():
    return html_login

@route('/login', method='POST')
def login_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    cur.execute("SELECT * FROM lab5.user_acc WHERE username = %s;" % username)
    user_credential = cur.fetchall()
    print user_credential

run(host='localhost', port=8081, debug=True)