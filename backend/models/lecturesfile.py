# models/lecture_file.py

from . import db

class LectureFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)

    def __repr__(self):
        return f'<LectureFile {self.filename}>'
