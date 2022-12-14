from flask.views import MethodView
from flask import make_response, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from extension import db
from db.user import User
from db.RevokedToken import RevokedToken


class Register(MethodView):
    """This class registers a new user."""
    
    def post(self):
        """Handle POST request for this view. Url --> /api/v1/auth/register"""
        # getting JSON data from request
        post_data = request.get_json(silent=True,force=True)

        try:
            name = post_data["name"]
            username = post_data["username"]
            email = post_data["email"]
            password = post_data["password"]
            password2 = post_data["password2"]
        except KeyError as err:
            response = {
                "success": False,
                "msg": f'{str(err)} key is not present'
            }
            return make_response(jsonify(response)), 400

        if password != password2:
            response = {
                "success": False,
                "msg": "Both passwords does not match"
            }
            return make_response(jsonify(response)), 400
        
        """Save the new User."""
        try:
            user = User(email=email, 
                        password=password, 
                        name=name, 
                        username=username)
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            print("Error occured: ", err)
            response = {
                "success": False,
                "msg": "Something went wrong!!"
            }
            return make_response(jsonify(response)), 500

        response = {
                    "success": True,
                    "msg": "You registered successfully. Please log in.",
                    "body": user
                    }

        # return a response notifying the user that they registered
        # successfully
        return response, 201


class Login(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /api/v1/auth/login/"""
        data = request.get_json(silent=True,
                                force=True)
        try:
            email = data["email"]
            password = data["password"]
        except KeyError as err:
            response = {
                "success": False,
                "msg": f'{str(err)} key is not present'
            }
            return make_response(jsonify(response)), 400
        
        # Get the user object using their email (unique to every user)
        # print(dir(User.User))
        user = User.query.filter_by(email=email).first()
        if not user:
            # User does not exist. Therefore, we return an error msg
            response = {
                "success": False,
                "msg": "Invalid email, Please try again"
            }
            return make_response(jsonify(response)), 400

        # Try to authenticate the found user using their password
        if not user.verify_password(password):
            response = {
                "success": False,
                "msg": "Wrong password, Please try again"
            }
            return make_response(jsonify(response)), 402

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        if not access_token or not refresh_token:
            response = {
                "success": False,
                "msg": "Something went wrong!"
            }
            # Return a server error using the HTTP Error Code 500 (Internal
            # Server Error)
            return make_response(jsonify(response)), 500
        
        # Generate the access token. This will be used as the
        # authorization header
        response = {
            "success": True,
            "msg": "You logged in successfully.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "body": user,
        }
        return make_response(jsonify(response)), 200

userController = {
    "register": Register.as_view("register"),
    "login": Login.as_view("login"),
}