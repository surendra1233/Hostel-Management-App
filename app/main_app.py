from app import app,db
from app.models import User,Post,Group,memb,Comment,likes,Room

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Group': Group , 'memb' : memb, 'Comment' : Comment , 'likes' : likes ,'Room' : Room }