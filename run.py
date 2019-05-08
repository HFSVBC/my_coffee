from flask import Flask, request, redirect, render_template, g
import webbrowser, sys, json, urllib, sqlite3
from os.path import isfile

app = Flask(__name__, static_url_path='')

### ROUTES
@app.route('/')
def index():
  return redirect("/home", code=302)

@app.route('/home')
def pageLoader():
  return render_template('home.html', users=getCoffeesPerUserInfo())

@app.route('/users/<int:id>')
def user(id):
  return render_template('user.html', user=getUser(id))

@app.route('/users/new', methods=['GET', 'POST'])
def newUser():
  if request.method == 'POST':
    name = request.form.get('name')
    credits = request.form.get('credits', 0)
    addUser(name, credits * 10)
    return redirect("/home", code=302)
  else:
    return render_template('newUser.html')

@app.route('/users/<int:id>/update_credits')
def updateCreditsToUser(id):
  updateCredits(id, request.values.get('credits', 0) * 10)
  return redirect("/users/{}".format(id), code=302)

@app.route('/users/<int:id>/coffees/add')
def addCoffee(id):
  increaseCoffee(id)
  return redirect("/home", code=302)

@app.route('/users/<int:id>/coffees/subtract')
def subtractCoffee(id):
  decreaseCoffee(id)
  return redirect("/home", code=302)

### DATA
def getCoffeesPerUserInfo():
  sql = """
    SELECT users.id, users.name, users.credits AS credits_left,
       users.credits AS coffees_left, users.credits_spent
    FROM users
  """
  return select_data(sql)

def getUser(id):
  sql = """
    SELECT users.id, users.name, users.credits AS credits_left,
       users.credits_spent AS coffees_consumed,
       users.credits AS coffees_left, users.credits_spent
    FROM users
    WHERE users.id = '{}'
  """.format(id)
  return select_data(sql, True)

def addUser(name, credits):
  sql = """
      INSERT INTO users (name, credits)
      VALUES('{}', '{}')
    """.format(name, credits)
  insert_data(sql)

def updateCredits(id, credits):
  sql = """
      UPDATE users
      SET credits = credits + '{}'
      WHERE id = '{}'
    """.format(credits, id)
  insert_data(sql)

def increaseCoffee(id):
  sql = """
    UPDATE users
    SET credits = credits - 1, credits_spent = credits_spent + 1
    WHERE id = '{}'
  """.format(id)
  insert_data(sql)

def decreaseCoffee(id):
  sql = """
    UPDATE users
    SET credits = credits + 1, credits_spent = credits_spent - 1
    WHERE id = '{}'
  """.format(id)
  insert_data(sql)

### DATABASE
def connect_db(database):
  db_is_created = isfile(database)
  g.conn = sqlite3.connect(database)
  g.cursor = g.conn.cursor()

  if not db_is_created:
    with open("my_coffee.sql", "r") as fp:
      query = fp.read()
      g.cursor.executescript(query)
      g.conn.commit()

@app.before_request
def before_request():
  g.db = connect_db('my_coffee.db')

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def insert_data(sql):
  g.cursor.execute(sql)
  g.conn.commit()

def select_data(sql, one=False):
  g.cursor.execute(sql)
  result =  g.cursor.fetchall()
  return (result[0] if result else None) if one else result

if __name__ == '__main__':
  app.run(threaded=True, host='0.0.0.0')