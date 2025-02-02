from flask import request, jsonify
from ..models import Customer
from datetime import datetime
from app import db
from . import api

@api.route("/customer", methods=['POST'])
def create_customer():
    data = request.get_json()

    required_fields = ['name', 'email', 'phone']
    missing_field = [field for field in required_fields if field not in data]

    if not data or missing_field:
        return jsonify({
            "message": f"required fields are missing: {", ".join(missing_field)}"
        }), 400
    
    new_customer =  Customer(
        name=data["name"],
        email=data["email"],
        phone=data["phone"]
    )

    existing_customer = Customer.query.filter((Customer.email==data["email"]) | (Customer.phone==data["phone"])).first()
    if existing_customer:
        return jsonify({"error": "Email or phone number already exists."}), 400
    
    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({
            "message": "customer added successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": f"could not add customer: {e}"
        }), 500
    
@api.route("/customer/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    customer = Customer.query.get(customer_id)
    if not Customer.query.filter(Customer.id==customer_id).first():
        return jsonify({"message": "Customer not found"}), 400
    elif not data:
        return jsonify({
            "message": "Not data found"
        }), 400
    
    if 'name' in data and data["name"]:
        customer.name = data['name']
    elif 'email' in data and data["email"]:
        customer.email = data.get('email')
    elif not 'phone' in data:
        customer.phone = data.get('phone', Customer.phone)

    customer.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({
            "message": f'Customer id:{customer_id} was updated'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": f"error when updating the Customer id:{customer_id}, error: {e}"
        }), 500
    

@api.route("/customer/<int:customer_id>", methods=['DELETEE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({
            "message": f"Customer not found"
        }), 404
    
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({
            "message": f"Customer id:{customer_id} was deleted sucessfully!"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": f"error when deleting the Customer id:{customer_id}, error: {e}"
        })

@api.route("/customer/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    try:
        customerID = Customer.query.get(customer_id)
        if not customerID:
            return jsonify({"message": "Customer not exists"}),500
        customer = {
           "name": customerID.name,
           "email": customerID.email,
           "phone": customerID.phone,
           "created_at": customerID.created_at 
        }
        return jsonify(customer), 200
    except Exception as e:
        db.rollback()
        return jsonify({
            "message": "an error occurred when bringing in a customer" 
        }), 500


@api.route("/customers", methods=["GET"])
def get_customers():
    try:
        customers = Customer.query.all()
        customers_list = [{
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'created_at': customer.created_at
        } for customer in customers]
        return jsonify(customers_list), 200
    except Exception as e:
        return jsonify({"message": "I can't get customers"}), 500