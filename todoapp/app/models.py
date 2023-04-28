from app import db
from app import datetime


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, default=datetime.utcnow)

    def format_date(self):
        return self.due_date.strftime('%d-%m-%Y')
    