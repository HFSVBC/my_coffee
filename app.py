import os
from datetime import datetime
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from  models import *

@app.route('/')
def index():
  return redirect("/home", code=302)

@app.route('/home')
def pageLoader():
  return render_template('home.html', users=getUsers())

@app.route('/users/<int:id>')
def user(id):
  return render_template('user.html', user=getUser(id))

@app.route('/users/new', methods=['GET', 'POST'])
def newUser():
  if request.method == 'POST':
    now = datetime.now()
    user = User(
      name=request.form.get('name'),
      credits=int(float(request.form.get('credits', 0)) * 10),
      created_at=now,
      updated_at=now
    )
    insert_data(user)
    return redirect("/home", code=302)
  else:
    return render_template('newUser.html')

@app.route('/users/<int:id>/update_credits')
def updateCreditsToUser(id):
  user = User.query.filter_by(id=int(id)).first()
  user.credits += int(float(request.values.get('credits', 0)) * 10)
  db.session.commit()
  return redirect("/users/{}".format(id), code=302)

@app.route('/users/<int:id>/coffees/add')
def addCoffee(id):
  now = datetime.now()
  coffee = Coffee(
    user_id=int(id),
    created_at=now,
    updated_at=now
  )
  insert_data(coffee)
  return redirect("/home", code=302)

@app.route('/users/<int:id>/coffees/subtract')
def subtractCoffee(id):
  coffee = Coffee.query.filter_by(user_id=int(id)).order_by(Coffee.created_at.desc()).first()
  delete_data(coffee)
  return redirect("/home", code=302)

### DATA
def getUsers():
  sql = """
    SELECT users.id, users.name, ROUND(COUNT(coffees.user_id) * 0.1, 2) AS credits_spent, 
      ROUND((users.credits - COUNT(coffees.user_id)) * 0.1, 2) AS credits_left, 
      users.credits - COUNT(coffees.user_id) AS coffees_left
    FROM users
    LEFT JOIN coffees ON coffees.user_id = users.id
    GROUP BY users.id, users.name, users.credits, coffees.user_id
  """
  return db.engine.execute(sql)

def getUser(id):
  sql = """
    SELECT users.id, users.name, ROUND(COUNT(coffees.user_id) * 0.1, 2) AS credits_spent, 
      ROUND((users.credits - COUNT(coffees.user_id)) * 0.1, 2) AS credits_left, 
      users.credits - COUNT(coffees.user_id) AS coffees_left,
      COUNT(coffees.user_id) AS coffees_consumed
    FROM users
    LEFT JOIN coffees ON coffees.user_id = users.id
    WHERE users.id = {}
    GROUP BY users.id, users.name, users.credits, coffees.user_id
  """.format(id)
  return db.engine.execute(sql).first()

### DATABASE
def insert_data(object):
  db.session.add(object)
  db.session.commit()

def delete_data(object):
  db.session.delete(object)
  db.session.commit()

if __name__ == "__main__":
  app.run(threaded=True, host='0.0.0.0')