from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Customer, Order
from app.sms_service import send_sms_notification

api_bp = Blueprint('api', __name__)

@api_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'code': c.code
    } for c in customers])

@api_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        code=data['code']
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@api_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'customer_id': o.customer_id,
        'item_name': o.item_name,
        'quantity': o.quantity,
        'price': o.price,
        'timestamp': o.timestamp.isoformat()
    } for o in orders])

@api_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    order = Order(
        customer_id=data['customer_id'],
        item_name=data['item_name'],
        quantity=data['quantity'],
        price=data['price']
    )
    db.session.add(order)
    db.session.commit()
    
    # Send SMS notification
    message = f"Hello {customer.name}, your order for {order.quantity} {order.item_name} has been received. Total: {order.price * order.quantity}"
    send_sms_notification(customer.phone, message)
    
    return jsonify({'message': 'Order created successfully'}), 201