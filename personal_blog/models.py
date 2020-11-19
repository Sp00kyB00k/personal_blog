from datetime import datetime
from personal_blog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    posts = db.relationship('Post', backref=db.backref("author", lazy=True))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    db.relationship('Role', backref=db.backref("assignee", lazy=True))

    def __repr__(self):
        return 'User {}'.format(self.username)


class Role(db.Model):
    id = db.column(db.Integer)
    rolename = db.Column(db.String(20), unique=True, nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return "{} : {}".format(self.title, self.body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "Category : {}".format(self.name)
