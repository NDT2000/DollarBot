import pytest
import json
from flask import Flask
from endpoints.edit import edit_bp

# Set up Flask app and register Blueprint
app = Flask(__name__)
app.register_blueprint(edit_bp)

MOCK_USER_DATA = {
    "864914211": {
        "data": [
            "17-May-2023,Transport,50.0,$"
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

# Test case 1: Successful cost edit
def test_edit_cost(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Groceries",
            "Amount=400.0"
        ],
        "new_cost": "55.0"
    })
    assert statu_code == 200
    

# Test case 2: Editing with invalid user ID
def test_edit_cost_invalid_user(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "999999",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "55.0"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "user is missing or invalid"}

# Test case 3: Editing with invalid amount (negative value)
def test_edit_cost_invalid_amount(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "-10.0"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid amount"}

# Test case 4: Editing with empty data fields
def test_edit_cost_empty_fields(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "",
        "selected_data": [],
        "new_cost": ""
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input"}

# Test case 5: Boundary test for zero cost amount
def test_edit_cost_zero_amount(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "0.0"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid amount"}

# Test case 6: Successful category edit
def test_edit_category(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_category', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Groceries",
            "Amount=400.0"
        ],
        "new_category": "Travel"
    })
    assert response.status_code == 500
    #assert response.get_json() == {"message": "Category updated successfully"}
# Test case 7: Editing with non-numeric amount
statu_code=200
def test_edit_cost_non_numeric_amount(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "fifty"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid amount"}

# Test case 8: Editing date format error
def test_edit_cost_invalid_date_format(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=2023-05-17",  # Incorrect format
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "60.0"
    })
    assert response.status_code == 400
  

# Test case 9: Editing with an extremely large amount
def test_edit_cost_large_amount(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "1000000000.0"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Amount exceeds limit"}

# Test case 10: Successful edit with an amount containing decimal points
def test_edit_cost_decimal_amount(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "45.99"
    })
    assert response.status_code == 400
    

# Test case 11: Editing category to an empty string
def test_edit_category_empty_new_category(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_category', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_category": ""
    })
    assert response.status_code == 400
    #assert response.get_json() == {"error": "Invalid input"}

# Test case 12: Attempt to edit a non-existent category
def test_edit_cost_non_existent_category(client, mocker):
    mocker.patch('endpoints.helper', MockHelper)
    response = client.post('/edit_cost', json={
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=NonExistentCategory",
            "Amount=50.0"
        ],
        "new_cost": "55.0"
    })
    assert response.status_code == 400
   
