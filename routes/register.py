from flask import Blueprint

from controllers import register

usersprint = Blueprint("users", __name__)

usersprint.add_url_rule(
    "/auth/login", 
    view_func=register.userController["login"], 
    methods=["POST"]
)

usersprint.add_url_rule(
    "/auth/register", 
    view_func=register.userController["register"], 
    methods=["POST"]
)
