from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_collaborator = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, email, password, is_admin, is_collaborator):
        self.name = name
        self.email = email
        self.hash = password
        self.is_admin = is_admin
        self.is_collaborator = is_collaborator


class Worksheet_Content(db.Model):
    __tablename__ = 'worksheet_content'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    person = db.Column(db.String(255))
    content = db.Column(db.JSON, nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    image_id = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title, company, person, content, creation_date, image_id):
        self.title = title
        self.company = company
        self.person = person
        self.content = content
        self.creation_date = creation_date
        self.image_id = image_id