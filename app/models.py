from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    blogs = db.relationship('Blogsite', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot access this property')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def update_user(self):
        db.session.add(self)
        db.session.commit()
        
class Blogsite(db.Model):
    __tablename__ = 'Blogsite'
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255))
    content = db.Column(db.String(255))
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='Blogsite', lazy='dynamic')

    def save_Blogsite(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls, category):
        blogs = Blogsite.query.filter_by(category_id=category)
        return blogs

    @classmethod
    def get_Blogsite_by_id(cls, id):
        Blogsite = Blogsite.query.filter_by(id=id).first()
        return Blogsite


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    Blogsite_id = db.Column(db.Integer, db.ForeignKey('Blogsite.id'))

    @classmethod
    def get_all_comments(cls, id):
        comments = Comment.query.filter_by(Blogsite_id= id).all()
        return comments

