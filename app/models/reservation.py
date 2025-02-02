from app import db
from enum import Enum

def datetime_now():
    return db.func.now()

class ReservationStatus(Enum):
    PENDING = 1
    RESERVED = 2
    FINISHED = 3

class Reservation(db.Model):

    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id')) #many to one
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id')) #many to one
    reservation_date = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=ReservationStatus.PENDING.value)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime_now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime_now())


    def __repr__(self):
        return f"<Customer: {self.customer_id}, Table: {self.table_id}>"