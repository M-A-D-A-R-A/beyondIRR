from datetime import datetime

from api.extensions import db

class Log(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  message = db.Column(db.String(120), nullable=False)
  type = db.Column(db.String(20), nullable=False)
  user_id = db.Column(db.Integer, nullable=False)
  username = db.Column(db.String(20), nullable=False)
  post_id = db.Column(db.Integer, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __init__(self, message, type,  user_id, post_id, username):
    self.message = message
    self.type = type
    self.user_id = user_id
    self.post_id = post_id
    self.username = username