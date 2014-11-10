import psycopg2

class Datastore:
  def __init__(self):
    print "(Datastore): Attempting to connect to datastore"
    database = psycopg2.connect(database='201201217', user='201201217', password='201201217',host='10.100.71.21', port='5432').cursor()    
    print "(Datastore): Datastore connected successfully"
    
  def is_existing_user(self, username):
    users = database.execute("SET SEARCH_PATH to lab5; SELECT username FROM user_acc").fetchall()
    for user in users:
      if user == username:
        return False
    return True
    
  def get_all_users(self):
    users = database.execute("SET SEARCH_PATH to lab5; SELECT username FROM user_acc").fetchall()
    result = []
    for user in users:  
      result.append(user)
    return result