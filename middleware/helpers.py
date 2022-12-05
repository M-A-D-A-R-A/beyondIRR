"""
In this file we are creating an islogin decoretor 
for finding if the user is valid or not by sending
a jwt token in headerfile of application, each time
when the user is requesting an api where he is dealing
with some sensitive information, each time we are going to
add this decoretor in particular routes function.
"""
from flask_restful import abort  #  functions abort for sending error message
from flask import request  #  for requesting header if jwt is present or not
from functools import wraps  #  wrap for creating decoretor
import jwt  # jwt for creating token
from api import app
from db.log import Log #  importing log model 
from db.user import User
from db.post import Post
from flask_jwt_extended import get_jwt_identity
from extension import db


#  creating islogin decorator
def islogin(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        auth = request.cookies.get('auth')  # checking if auth is present in request header/ cookies
        
        #  if present 
        if auth:
            user = jwt.decode(auth, algorithms=['HS256'], key=app.config['SECRET_KEY'])
            user_id = user['user_id']

        else:
            # if not present
            abort(404, message="you are not login")
        return f(user_id, *args, **kwargs)
    return wrap
    
# Use this decorator on users and posts routes for tracking activity
def record_logs(fun):
  @wraps(fun)
  def wrap(*args, **kwargs):
    
    try:
      result = fun(*args, **kwargs)
      status_code = int(result[1])
      
      # If unsuccessful request then no need to store log
      if status_code != 200 and status_code != 201:
        return result

      # Get user details
      user_id = get_jwt_identity()
      user = User.query.filter_by(id=user_id).first()

      # Get url, method and post_id
      url = request.path
      method = request.method
      post_id = kwargs.get('post_id') if kwargs.get('post_id') else -1
      post = Post.query.filter_by(id = post_id).first()
      # Initialize with default values
      message = url
      post_type = ''

      if url == f'/api/v1/auth/register':
        if method == 'POST':
          message = f'New user added  {user["username"]}'
      
      if url == f'/api/v1/auth/login/':
        if method == 'POST':
          message = f'{user["username"]} logged in'
      
      if url == f'/api/v1/post/{user_id}':
        if method == 'POST': 
          message = f'{user["username"]} posted someting'
      if url == f'/api/v1/post/{user_id}/update/{post_id}':
        if method == 'PUT': 
          message = f'{user["username"]} updated {post["title"]}'
      
      log = Log(
        message=message, 
        user_id=user_id, 
        type=post_type,
        post_id= post_id,
        username=user['username'],
      )
      db.session.add(log)
      db.session.commit()
      return result
    
    except Exception as e:
      print('Error - ', str(e))
      return fun(*args, **kwargs)
  return wrap