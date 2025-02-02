from flask import jsonify, request
from app import db
from ..models import Table
from . import api

@api.route("/table", methods=['POST'])
def create_table():
    data = request.get_json()
    table_validation = Table.query.filter(Table.number==data["number"]).first()
    if table_validation:
        return jsonify({"message":"Table alredy exists"}), 400
    if not data:
        return jsonify("message", "not data found"), 400
    new_table = Table(
        number=int(data["number"]),
        seats=int(data.get("seats", 4)))
    try:
        db.session.add(new_table)
        db.session.commit()
        return jsonify({"message": "New table created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Could'nt created table"}), 400


@api.route("/table/<int:table_id>", methods=['DELETE'])
def delete_table(table_id:int):
    table = Table.query.get(table_id)
    if not table:
        return jsonify({"message": "table not found"}), 404
    
    try:
        db.session.delete(table)
        db.session.commit()
        return jsonify({"message":f"Table {table_id} was deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify("error when deleting the table id:{table_id}"), 500
    
@api.route("/table/<int:table_id>", methods=['GET'])
def get_table_by_id(table_id:int):
    try:
        tableID = Table.query.get(table_id)
        if not tableID:
            return jsonify({"message": "table not found"}), 404
        table = {"number": tableID.number, "seats":tableID.seats}
        return jsonify(table)
    except Exception:
        return jsonify({"message": f"Table {table_id} could not be recovered"}), 500


@api.route("/tables", methods=["GET"])
def get_tables() -> jsonify:
    try:
        tables = Table.query.all()
        table_list = [{
            "table": table.number,
            "seats": table.seats
        } for table in tables]
        return jsonify(table_list), 200
    except Exception as e:
        return jsonify({"message": "The tables could not be obtained"}), 500