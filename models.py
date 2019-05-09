from app import db

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False, unique=True)
  credits = db.Column(db.Integer(), nullable=False)
  created_at = db.Column(db.DateTime(), nullable=False)
  updated_at = db.Column(db.DateTime(), nullable=False)

  def __init__(self, name, credits, created_at, updated_at):
    self.name = name
    self.credits = credits
    self.created_at = created_at
    self.updated_at = updated_at
        

  def __repr__(self):
    return '<id {}>'.format(self.id)
    
class Coffee(db.Model):
  __tablename__ = 'coffees'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime(), nullable=False)
  updated_at = db.Column(db.DateTime(), nullable=False)

  def __init__(self, name, user_id, created_at, updated_at):
    self.name = name
    self.user_id = user_id
    self.created_at = created_at
    self.updated_at = updated_at
        

  def __repr__(self):
    return '<id {}>'.format(self.id)
    