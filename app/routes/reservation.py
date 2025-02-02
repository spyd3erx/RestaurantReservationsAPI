from app import db
from ..models import Reservation, Customer, Table
from ..models.reservation import ReservationStatus
from flask import request, jsonify
from . import api
from datetime import datetime, timedelta

@api.route('/reservation', methods=['POST'])
def make_reservation():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Not data foud"}), 400


    customer_id = data.get("customer_id")
    table_id = data.get("table_id")
    reservation_date = data.get("reservation_date")
    duration = data.get("duration_hours", 2)
    status = data.get("status", 1)


    if not all([customer_id, table_id, reservation_date]):
        return jsonify({"error": "missing fields required (customer_id, table_id, reservation_date)"}), 400

    try:
        reservation_datetime = datetime.fromisoformat(reservation_date)
    except ValueError:
        return jsonify({"error": "invalid date format, use 'YYYY-MM-DD HH:MM:SS'"}), 400

    # Calculate the end time of the new reservation
    end_time = reservation_datetime + timedelta(hours=duration)
    # Query for existing reservations with potential overlap
    existing_reservations = Reservation.query.filter(
        Reservation.table_id == table_id,  # Filtra por mesa
        Reservation.reservation_date < end_time,  # Reservas que comienzan antes del fin de la nueva reserva
        db.func.timestampadd(db.text('HOUR'), Reservation.duration, Reservation.reservation_date) > reservation_datetime  # Reservas que terminan después del inicio de la nueva reserva
    ).all()

    if existing_reservations:
        return jsonify({"error": "The table is not available for the requested time"}), 400

    new_reservation = Reservation(
        customer_id=customer_id,
        table_id=table_id,
        reservation_date=reservation_datetime,
        duration=duration,
        status=status
    )
    try:
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({
            "message": "Reservation successfully created",
            "reservation": {
                "id": new_reservation.id,
                "customer_id": new_reservation.customer_id,
                "table_id": new_reservation.table_id,
                "reservation_date": new_reservation.reservation_date.strftime("%Y-%m-%d %H:%M:%S"),
                "durations": new_reservation.duration,
                "status": Reservation(new_reservation.status).name.title()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Couldn't create reservation in this moment\n{e}"}), 500


@api.route("/reservation/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    data = request.get_json()
    reservation = Reservation.query.get(reservation_id)
    if not data:
        return jsonify({"message": "no data found"}), 400
    if not reservation:
        return jsonify({"message": "No reservation exists"}), 400
    
    if 'status' in data and data['status']:
        reservation.status = data["status"]
    

    try:
        db.session.commit()
        return jsonify({"message": "reservation was update",
                        "id": reservation.id,
                        "status": ReservationStatus(reservation.status).name.title()})
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Can't update reservation"}), 500

@api.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        reservations = (
            db.session.query(Reservation)
            .join(Customer, Reservation.customer_id == Customer.id)
            .join(Table, Reservation.table_id == Table.id)
            .all()
        )

        result = []
        for reservation in reservations:
            result.append({
                "id": reservation.id,
                "reservation_date": reservation.reservation_date.isoformat(),
                "status": ReservationStatus(reservation.status).name.title(),
                "customer": {
                    "id": reservation.customer.id,
                    "name": reservation.customer.name,
                    "email": reservation.customer.email,
                    "phone": reservation.customer.phone,
                },
                "table": {
                    "id": reservation.table.id,
                    "number": reservation.table.number,
                    "seats": reservation.table.seats,
                },
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/reservation/<int:reservation_id>", methods=["GET"])
def reservation_by_id(reservation_id):
  try:
    reservationByID = (
        Reservation.query
        .join(Customer, Reservation.customer_id == Customer.id)
        .join(Table, Reservation.table_id == Table.id)
        .filter(Reservation.id == reservation_id)
        .first()
    )


    if not reservationByID:
      return jsonify({'error': 'Reservation not found'}), 404
    return jsonify({
        "id": reservationByID.id,
        "reservation_date": reservationByID.reservation_date.isoformat(),
        "status": ReservationStatus(reservationByID.status).name.title(),
        "customer": {
          "id": reservationByID.customer.id,
          "name": reservationByID.customer.name,
          "email": reservationByID.customer.email,
          "phone": reservationByID.customer.phone,
        },
        "table": {
          "id": reservationByID.table.id,
          "number": reservationByID.table.number,
          "seats": reservationByID.table.seats,
        }
    })
  except Exception as e:
    return jsonify({'error': 'Internal server error'}), 500