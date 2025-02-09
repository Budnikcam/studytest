from models.database import db

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Lecture {self.title}>'
