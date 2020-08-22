from app import db,login
from datetime import datetime
from werkzeug import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

memb = db.Table('memb',
	db.Column('status',db.Integer,default=0),	
	db.Column('group_id',db.Integer,db.ForeignKey('group.id')),
	db.Column('user_id',db.Integer,db.ForeignKey('user.id'))
	)

likes = db.Table('likes',
	db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
	db.Column('user_id',db.Integer,db.ForeignKey('user.id'))
	)

class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),index=True,unique=True)
	email = db.Column(db.String(32), index=True, unique=True)
	batch = db.Column(db.String(32), index=True, unique=False)
	city = db.Column(db.String(32), index = True,unique=False)	
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post',backref='author',lazy='dynamic')
	comments = db.relationship('Comment',backref='author',lazy='dynamic')
	groups = db.relationship('Group',secondary=memb,backref=db.backref('members',lazy='dynamic'))
	room = db.relationship('Room',backref='user',lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	group_id = db.Column(db.Integer,db.ForeignKey('group.id'))
	liker = db.relationship('User',secondary=likes,backref=db.backref('liked_posts',lazy='dynamic'))
	comments = db.relationship('Comment',backref='post',lazy='dynamic')
	status = db.Column(db.Integer,default=0)

	def __repr__(self):
		return '<Post {}>'.format(self.body)

class Group(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(32),index=True,unique=True)
	posts = db.relationship('Post',backref='group',lazy='dynamic')


class Comment(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.String(120))
	timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

class Room(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	roomno = db.Column(db.Integer)
