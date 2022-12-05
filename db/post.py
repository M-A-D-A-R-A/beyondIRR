from extension import db
type = ['draft','Archived','published']

class Post(db.Model):
    """
    This model holds information about a post
    """
    __tablename__ = "post"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=True)
    body = db.Column(db.String(1000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="cascade", onupdate="cascade"))
    type = db.Column(db.String(1000), nullable=True,default='draft')

       
