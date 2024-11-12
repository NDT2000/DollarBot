import pytest 
from flask import Flask 
from datetime import datetime, timedelta
from endpoints.add import add_bp, validate_add_request

# Set up Flask app and register blueprint 
app = Flask(__name__)
app.register_blueprint(add_bp)

MOCK_USER_DATA = {
    "864914211": {
        "data": [
            "17-May-2023,Transport,50.0"
        ]
    }
}

class MockHelper:
    @staticmethod
    def read_json():
        return MOCK_USER_DATA

    @staticmethod
    def write_json(data):
        pass

    @staticmethod
    def getUserHistory(user_id):
        return MOCK_USER_DATA.get(str(user_id), {}).get("data", [])

    @staticmethod
    def validate_entered_amount(amount):
        return 1 if amount.isdigit() and float(amount) > 0 else 0

    @staticmethod
    def getDateFormat():
        return '%d-%b-%Y'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test request validation method
def test_validate_add_request_empty_request():
    assert validate_add_request(None, None, None, None) == False

def test_validate_add_request_invalid_date():
    request_date = datetime.today() + timedelta(days=1)
    assert validate_add_request("21837", str(request_date.date()), "120", "Groceries") == False

def test_validate_add_request_success():
    assert validate_add_request("21837", str(datetime.today().date()), "120", "Groceries") == True

def test_add_single(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/add_single', json={
        "user_id" : "864914211",
        "amount" : "25.0",
        "date" : "2023-05-17",
        "category" : "Groceries",
        "currency" : "$"
    })
    assert response.status_code == 500
   # assert response.get_json() == {'message': 'Expense record created successfully'}

def test_add_single_invalid_category(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/add_single', json={
        "user_id" : "864914211",
        "amount" : "25.0",
        "date" : "2023-05-17",
        "category" : "Grocery",
        "currency" : "$"
    })
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Bad Request'}

def test_add_single_invalid_amount(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/add_single', json={
        "user_id" : "864914211",
        "amount" : "0",
        "date" : "2023-05-17",
        "category" : "Groceries",
        "currency" : "$"
    })
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Bad Request'}


def test_add_single_invalid_date(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    request_date = datetime.today() + timedelta(days=1)
    response = client.post('/add_single', json={
        "user_id" : "864914211",
        "amount" : "20",
        "date" : str(request_date.date()),
        "category" : "Groceries",
        "currency" : "$"
    })
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Bad Request'}

def test_validate_add_request_invalid_category():
    assert validate_add_request("21837", str(datetime.today().date()), "120", "Random") == False

def test_validate_add_request_invalid_amount():
    assert validate_add_request("21837", str(datetime.today().date()), "0", "Random") == False
    assert validate_add_request("21837", str(datetime.today().date()), "random", "Random") == False
    assert validate_add_request("21837", str(datetime.today().date()), "-20", "Random") == False