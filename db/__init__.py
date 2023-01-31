import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()


class Severity(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class Status(enum.Enum):
    new = 'new'
    in_progress = 'in progress'
    done = 'done'


class Ticket(db.Model):
    """
    Model for Ticket table
    """
    __tablename__ = "ticket"
    ticket_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)
    severity = db.Column('severity', db.Enum(Severity), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)

    def json(self):
        values = self.__dict__
        dict_values = {'title': values['title'],
                       'description': values['description'],
                       'severity': values['severity'].value,
                       'status': values['status'].value,
                       'ticket_id': values['ticket_id']}
        return dict_values
