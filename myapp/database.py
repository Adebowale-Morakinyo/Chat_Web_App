from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(5), nullable=False) # data formatted in the client script already

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'message': self.message, 'time': self.time}
