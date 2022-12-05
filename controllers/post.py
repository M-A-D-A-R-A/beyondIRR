from os import abort
from flask.views import MethodView
from flask import make_response, request, jsonify, current_app

from extension import db
from db.post import Post

allowed_types = ['draft','Archived','published']


class AddPost(MethodView):
    """
    This class-based view Adds a post for the user
    Url --> /api/v1/post/<int:user_id>
    """
    # @islogin
    def post(self,user_id):
        #  request body
        if not user_id:
                response = {
                    "success":False,
                    "msg": "user id not provided"
                }
                return make_response(jsonify(response)), 400
        
        data = request.get_json(silent=True,
                                force=True)
        post_title = data["title"]
        post_body = data["body"]
        post_type = data["type"]

        is_title_exist = Post.query.filter_by(title=post_title).first()
        if is_title_exist:
            abort(404, message="Title is already taken, please try another one")
        
        if post_type in allowed_types:
            post = Post(title=post_title, body=post_body, user_id=user_id,type=post_type)
        else:
            post = Post(title=post_title, body=post_body, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post,200


class UpdatePost(MethodView):
    """
    This class-based view Adds a post for the user
    Url --> /api/v1/post/<int:user_id>/update/<int:post_id>
    """
    # @islogin
    def put(self,user_id,post_id):
        #  request body
        if not user_id:
                response = {
                    "success":False,
                    "msg": "user id not provided"
                }
                return make_response(jsonify(response)), 400
        if not post_id:
                response = {
                    "success":False,
                    "msg": "post id not provided"
                }
                return make_response(jsonify(response)), 400
        data = request.get_json(silent=True,
                                force=True)
        post_title = data["title"]
        post_body = data["body"]
        post_type = data["type"]

        is_title_exist = Post.query.filter_by(title=post_title).first()
        if is_title_exist:
            abort(404, message="Title is already taken, please try another one")
        
        if data["type"]:
            post = Post(title=post_title, body=post_body, user_id=user_id,type=post_type)
        else:
            post = Post(title=post_title, body=post_body, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post,200

class FetchtypePostView(MethodView):

    """
    This route fetches all post  of a particular type
     URL:- /api/v1/post/<int:post_id>/type/<string:type>
    """
    def get(self,post_id, type):
        try:
            if not post_id:        
                response = {
                    "success": False,
                    "msg": "Provide the post_id.",
                }
                return make_response(jsonify(response)), 422
            
            if type not in allowed_types:  
                response = {
                    "success": False,
                    "msg": "Invalid type"
                }
                return make_response(jsonify(response)), 422
            
            post_type =  Post.query.filter_by(id=post_id, type=type)

            response = {
                'success':True,
                'data':post_type
            }
            return make_response(jsonify(response)), 200

        except Exception:
            response = {
                "success":False,
                "msg": "Something went wrong!"
                }
            # Return a server error using the HTTP Error Code 500 (Internal
            # Server Error)
            return make_response(jsonify(response)), 500

postController = {
    "userPost": AddPost.as_view("userPost"),
    "fetchTypePost": FetchtypePostView.as_view("fetchtypepost"),
    "updatePost":UpdatePost.as_view("updatepost")
}