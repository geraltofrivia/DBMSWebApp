from bottle import route, run, get, post, request, response
from bottle import jinja2_view, route
from bottle import static_file
import psycopg2

database = psycopg2.connect(database='201201217', user='201201217', password='201201217',host='10.100.71.21', port='5432')
cur = database.cursor()
print "Database initialized "

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

html_contests = '''
<html>
  <head>
    <title></title>
    <meta content="">
    <style></style>
  </head>
  <body>
    <h2> Contests </h2> <br> <hr>
    <p> Contests are an integral part of this website.
    We believe that a healthy competition acts as a booster for anyone who inspires to push his skill set to the limits <br>
    In the age of information, we are all but walking repositories of knowledge waiting to be tested. Gradually we shed what we seem not to require<br>
    Ask yourself, when did you put yourself under some test of that knowledge of the algorithms and the frameworks you learnt overtime from countless books and websites, only to never work upon them ever?<br>
    <br>
    We understand and appreciate the kind of attitude people have towards programming. For the definition of this word grew from teaching large chunky machines where to punch holes appropriately to running mighty websites from a credit card sized computer<br>
    To respect every taste towards this branch, we provide two basic divisions in the kind of activities you could involve yourself with</p><br>
    <a href = '/pcontests'><div style="width:500px; height:100px; margin:10px; background-color:#FF4940"> Programming contests</div> </a>
    <a href = '/dcontests'><div style="width:500px; height:100px; margin:10px; background-color:#FFB561"> Developing contests</div> </a>
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
    username= request.get_cookie("username")
    print "I am %s" % username
    for user in l_users:
        if username == user[0]:
            usernames += "<li> <a href=='/users/%s>" % username + user[0] + '</a>'
            continue
        usernames += '<li>' + user[0]
        print user[0]
    result = html_users % usernames
    return result

@route('/login')
def login():
    return html_login

@route('/login', method='POST')
def login_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    cur.execute("SELECT * FROM lab5.user_acc WHERE username = '%s';" % username)
    user_credential = cur.fetchall()
    print user_credential
    if not user_credential:
        return login()
    if user_credential[0][1] == password:
        print "logging in %s" % username
        response.set_cookie("username", "ratbumpy")
        return "YOU HAVE NOW SUCCESSFULLY LOGGED IN<br>Though as of now that doesn't grant you access to anything because we just haven't figured out a way to send cookies over this framework so, yeah. <sarcasm> Yay </sarcasm>"
    else:
        print "Incorrect credentials"
        return login()

@route('/contests')
def contests():
    return html_contests


@route('/hello')
def hello_again():
    if request.get_cookie("visited"):
        return "Welcome back! Nice to see you again"
    else:
        response.set_cookie("visited", "yes")
        return "Hello there! Nice to meet you"

@route('/logout')
def logout():
    if request.get_cookie("username"):
        response.delete_cookie("username")

@route('/check_login')
def is_loggedin():
    if request.get_cookie("username"):
        return request.get_cookie("username")


run(host='localhost', port=8081, debug=True)
