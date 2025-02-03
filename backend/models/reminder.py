from backend.models.database import db

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    reminder_date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Reminder for lecture ID {self.lecture_id}>'
