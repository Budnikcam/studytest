from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50)) 
    content = db.Column(db.Text)
    
    
    files = db.relationship('LectureFile', backref='lecture', lazy=True) 

class LectureFile(db.Model):
    __tablename__ = 'lecture_files' 

    id = db.Column(db.Integer, primary_key=True)  
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)  
    filename = db.Column(db.String(255), nullable=False)  
    filepath = db.Column(db.String(255), nullable=False)  

   
    lecture = db.relationship('Lecture', back_populates='files')
