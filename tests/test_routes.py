import pytest
from app import create_app, db
from app.models import Customer, Order
from datetime import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add test data
            customer = Customer(
                name="Test User",
                email="test@example.com",
                phone="+254700000000",
                code="TEST001"
            )
            db.session.add(customer)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_customers(client):
    response = client.get('/api/customers')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == "Test User"

def test_create_order(client):
    data = {
        'customer_id': 1,
        'item_name': 'Test Item',
        'quantity': 2,
        'price': 10.0
    }
    response = client.post('/api/orders', json=data)
    assert response.status_code == 201
    assert response.json['message'] == 'Order created successfully'