from app import db
from datetime import datetime

class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.utcnow)
    reservations = db.relationship("Reservation", backref="customer") #one to many

    def __repr__(self):
        return f"<Customer: {self.name}, {self.email}>"