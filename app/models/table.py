from app import db

class Table(db.Model):

    __tablename__ = "tables"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)
    reservations = db.relationship("Reservation", backref="table") #one to many

    def __repr__(self):
        return f"<Table #{self.number}>"