from flask import Blueprint

from controllers import post

postsprint = Blueprint("posts", __name__)

postsprint.add_url_rule(
    "/post/<int:user_id>", 
    view_func=post.postController["userPost"], 
    methods=["POST"]
)

postsprint.add_url_rule(
    "post/<int:post_id>/type/<string:type>", 
    view_func=post.postController["fetchtypepost"], 
    methods=["POST"]
)
postsprint.add_url_rule(
    "post/<int:user_id>/update/<int:post_id>", 
    view_func=post.postController["updatepost"], 
    methods=["PUT"]
)
