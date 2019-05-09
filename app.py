import os
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from  models import *

@app.route('/')
def index():
  return redirect("/home", code=302)

@app.route('/home')
def pageLoader():
  # users=getCoffeesPerUserInfo()
  return render_template('home.html', users=[])

@app.route('/users/<int:id>')
def user(id):
  # user=getUser(id)
  return render_template('user.html', user=[])

@app.route('/users/new', methods=['GET', 'POST'])
def newUser():
  if request.method == 'POST':
    name = request.form.get('name')
    credits = request.form.get('credits', 0)
    # addUser(name, float(credits) * 10)
    return redirect("/home", code=302)
  else:
    return render_template('newUser.html')

@app.route('/users/<int:id>/update_credits')
def updateCreditsToUser(id):
  # updateCredits(id, float(request.values.get('credits', 0)) * 10)
  return redirect("/users/{}".format(id), code=302)

@app.route('/users/<int:id>/coffees/add')
def addCoffee(id):
  # increaseCoffee(id)
  return redirect("/home", code=302)

@app.route('/users/<int:id>/coffees/subtract')
def subtractCoffee(id):
  # decreaseCoffee(id)
  return redirect("/home", code=302)

### DATABASE
def insert_data(object):
  db.session.add(object)
  db.session.commit()

def select_data():
  pass

if __name__ == "__main__":
  app.run(threaded=True, host='0.0.0.0')