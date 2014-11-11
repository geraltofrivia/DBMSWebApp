from bottle import route, run, get, post, request, response
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
        <h2> <a href="/"> Users </a> </h2> <br> <hr>
        <ul>
            %s
        </ul> 
	</body> 
</html>
'''

html_register = '''
<html>
  <head>
    <title></title>
    <meta content="">
    <style></style>
  </head>
    <body> 
        <form method = 'post'>
            <br>
            <label> <h2> Register. </h2> 
                <hr> 
                <br> Enter your details below 
            </label> 
            <br>
            <label> Name </label> <input type="text" name="username"> </label> <br>
            <label> Password </label> <input type="password" name="password"> </label> <br>
            <label> Retype Password </label> <input type="password" name="password_r"> </label> <br>
            <input type="submit">
        </form>
    </body> 
</html>'''


html_home = '''
<html>
  <head>
    <title>Competition Organizer</title>
    <meta content="">
    <style></style>
  </head>
  <body>
  <h1> Home </h1> <hr> <br>
  <p>Please find yourself at home on this website. 
  We have tried our best to provide you with a reliable system that puts your time and efforts to good use, sharpening your programming skills which may help you build your part towards a better tomorrow
  <br>
  Welcome aboard!</p>
  
  <a href="/login"> Login </a> | <a href="/register"> Register </a> <br>
  <div> <a href="/users"> View all users </a> </div>
  <div> <a href="/contests"> Or jump right in! </a> </div>
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
    <h2> <a href="/"> Login </a> </h2> <br> <hr>
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
    <h2> <a href="/"> Contests </a> </h2> <br> <hr>
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

html_dcontests = '''
<html>
  <head>
    <title></title>
    <meta content="">
    <style></style>
  </head>
  <body>
    <h2> <a href="/"> Developing Contests </a> </h2> <br> <hr>
    <p> Developing contests are designed to put to test if you are capable of developing a complete software/website/extension. <br>This kind of contest is radically different than programming contests for this does not stress on your algorithmic skills as much as it tests your knowledge and practice of handling frameworks and APIs as well as immense amount of creativity<br>
    You may contact the mentors if you ever feel the need to. </p> <br>
    <h4> Open Contests </h4>
    <p> These contests have been declared open, but the activities haven't yet begun. Now would be a nice time to start </p>
    <ul> %(open)s </ul>
    <h4> Active Contests </h4>
    <p> Although they have begun, they have not yet ended. Don't let doubt take the best of you. Start now!</p>
    <ul> %(active)s </ul>
    </body>
</html>'''
  
html_pcontests = '''
<html>
  <head>
    <title></title>
    <meta content="">
    <style></style>
  </head>
  <body>
    <h2> <a href="/"> Programming Contests  </a></h2> <br> <hr>
    <p> Programming contests are designed to challenge your algorithm skills. Please choose any contest from the list below and get going. 
    You may contact the mentors if you ever feel the need to. </p> <br>
    <h4> Open Contests </h4>
    <p> These contests have been declared open, but the activities haven't yet begun. Now would be a nice time to start </p>
    <ul> %(open)s </ul>
    <h4> Active Contests </h4>
    <p> Although they have begun, they have not yet ended. Don't let doubt take the best of you. Start now!</p>
    <ul> %(active)s </ul>
    </body>
</html>
'''    
    
@route("/")
def home():
  return html_home


@route('/register')
def register():
    return html_register

@route('/register', method='POST')
def register_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    password_r = request.forms.get('password_r')
    if len(username)>0 and len(password)>0 and len(password_r)>0:
        if password == password_r:
            cur.execute("INSERT INTO lab5.user_acc VALUES ('%(u)s', '%(p)s');" % {'u':username, 'p':password})
            database.commit()
            return "Successfully registered %s. <br> <a href='/'> << Go back </a>" % username
        else:
            return register()
    else:
        return register()
        

@route('/users')
def print_users():
    cur.execute("SELECT * FROM lab5.user_acc;")
    l_users = cur.fetchall()
    usernames = ''
    username= request.get_cookie("username")
    print "I am %s" % username
    for user in l_users:
        if username == user[0]:
            usernames += "<li> <a href='/user/%s'>" % username + user[0] + '</a>'
            continue
        usernames += '<li>' + user[0]
        print user[0]
    result = html_users % usernames
    return result

@route('/user/<user>')
def print_user(user):
    print user
    cur.execute("SELECT * FROM lab5.user_acc WHERE username = '%s';" % user)
    user_detail = cur.fetchall()
    result_user = ''
    if user_detail:
        result_user += "<h1> <b> <a href='/'>  %s </a></b> </h1><hr>" % user
        cur.execute("SELECT DISTINCT teamname, T.teamid FROM lab5.members as M, lab5.team as T WHERE username = '%s' and M.teamid = T.teamid ;" % user)
        teams = cur.fetchall()
        result_user += '<h4> Member of teams - </h4> <ul>' 
        result_team = ''
        for team in teams:
            result_team += '<li> <a href="/team/%s">' % team[1] + team[0] + '</a>'
        if len(result_team) < 1:
            result_team = '<li> None'
        result_user += result_team + '</ul>'
        result_user += '<h4> Top Scoring submissions </h4> <ul>'
        cur.execute("SELECT contestname, score, S.contestid FROM lab5.SUBMISSIONS as S, lab5.submits_user as Su, lab5.contests as C WHERE S.submissionid = Su.submissionid AND username = '%s' AND C.contestid = S.contestid ORDER BY score DESC LIMIT 3;" % user)
        result_sub = ''
        subs = cur.fetchall()
        for sub in subs:
            result_sub += '<li> <a href="/contests/%(link)s"> %(cname)s</a> - %(score)d ' % {'cname':sub[0], 'score':sub[1], 'link':sub[2]}
        if len(result_sub) < 1:
            result_sub = '<li> None'
        result_user += result_sub + '</ul>'
        result_user += '<b> #submissions - </b> '
        cur.execute("SELECT COUNT(submissionid) FROM lab5.SUBMITS_USER WHERE username = '%s';" % user)
        num_subs = cur.fetchall()[0]
        print num_subs
        result_user += str(num_subs)[1:-3]

        #If logged in with same user, give option to delete the user as well.
        if request.get_cookie("username") == user:
            result_user += "<br><br><br><a href='/delete/%s'> Click to delete user!. Beware that you can't undo this action </a>" % user
    else:
        return print_users()
    return result_user    

@route('/team/<team>')
def print_team(team):
    print team
    cur.execute("SELECT * FROM lab5.team WHERE teamid = '%s';" % team)
    team_detail = cur.fetchall()
    if len(team_detail) > 1:
        team_detail = team_detail[0]
    else:
        return home()
    result_team = ''
    print team_detail
    if team_detail:
        result_team += '<h1> <a href="/"> %s </a> </h1><hr>' % team_detail[0]
        cur.execute("SELECT username FROM lab5.TEAM as T, lab5.members as M where M.teamid = T.teamid AND teamname = '%s'" % team_detail[0])
        usernames = cur.fetchall()
        result_team += "<h4> Members - </h4> <ul>"
        for user in usernames:
            result_team += "<li> <a href='/user/%(userid)s'> %(usernm)s </a>" % {'userid':user[0], 'usernm':user[0]}
    else:
        return home()
    return result_team


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
        response.set_cookie("username", user_credential[0][0])
        return "Now successfully logged in as %s <br> <a href='/'> << Go Back </a>"  % user_credential[0][0]
    else:
        print "Incorrect credentials"
        return login()

@route('/contests')
def contests():
    return html_contests

@route('/pcontests')
def programming_contests():
    cur.execute("SELECT * FROM lab5.programmingContest as PC, lab5.contests as C WHERE PC.contestid =  C.contestid AND C.state = 'open';")
    opens = cur.fetchall()
    cur.execute("SELECT * FROM lab5.programmingContest as PC, lab5.contests as C WHERE PC.contestid =  C.contestid AND C.state = 'active';")
    active = cur.fetchall()
    html_open  = ''
    html_active = ''
    for contest in opens:
        html_open += '<li> ' + contest[2]
    for contest in active:
        html_active += '<li> ' + contest[2]  
    result = html_pcontests % {'open':html_open,'active':html_active}
    return result
        
@route('/dcontests')
def developing_cntests():
    cur.execute("SELECT * FROM lab5.developingContest as PC, lab5.contests as C WHERE PC.contestid =  C.contestid AND C.state = 'open';")
    opens = cur.fetchall()
    cur.execute("SELECT * FROM lab5.developingContest as PC, lab5.contests as C WHERE PC.contestid =  C.contestid AND C.state = 'active';")
    active = cur.fetchall()
    html_open  = ''
    html_active = ''
    for contest in opens:
        html_open += '<li> '+ contest[3]
    for contest in active:
        html_active += '<li> '+  contest[3]
    result = html_pcontests % {'open':html_open,'active':html_active}
    return result

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
        return 'Logged you out :) <br> Be back soon'
    else:
        return "You are not logged in, in the first place <br> <a href='/'> << Go Back </a>"

@route('/check_login')
def is_loggedin():
    if request.get_cookie("username"):
        return "You are logged in as %s. <br> <a href='/'> << Go Back </a>" % request.get_cookie("username")
    else:
        return "You are not logged in, in the first place <br> <a href='/'> << Go Back </a>"

@route('/delete/<user>')
def delete(user):
    username = request.get_cookie("username")
    if user:
        if user== username:
            print "HERE"
            cur.execute("DELETE FROM lab5.members WHERE username = '%s';" % user)
            cur.execute("SELECT * FROM lab5.submits_user WHERE username = '%s';" % user)
            submissionids = cur.fetchall()
            for s in submissionids:
                cur.execute("DELETE FROM lab5.submissions WHERE submissionid = '%s';" % s)
            cur.execute("DELETE FROM lab5.submits_user WHERE username = '%s';" % user)
            cur.execute("DELETE FROM lab5.sponsors WHERE username = '%s';" % user)
            cur.execute("DELETE FROM lab5.judges WHERE username = '%s';" % user)
            cur.execute("SELECT * FROM lab5.discussions WHERE username = '%s';" % user)
            discussions = cur.fetchall()
            for d in discussions:
                cur.execute("DELETE FROM lab5.comments WHERE discussionid = '%s';" % d)
            cur.execute("DELETE FROM lab5.discussions WHERE username = '%s';" % user)
            cur.execute("DELETE FROM lab5.user_acc WHERE username = '%s';" % user)

            database.commit()
            response.delete_cookie("username")
            return "%s now deleted from the Database" % user
        else:
            return "You are not logged in, in the first place <br> <a href='/'> << Go Back </a>"


run(host='localhost', port=8081, debug=True)
