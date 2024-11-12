from flask import Blueprint, request, jsonify
import  endpoints.helper as helper
from datetime import datetime


add_bp = Blueprint('add', __name__)


def validate_add_request(chat_id, expense_date, expense_amount, expense_category):
    # validate input request 
    if not chat_id or not expense_date or not expense_category or not expense_amount:
        return False
    if datetime.strptime(expense_date, '%Y-%m-%d').date() > datetime.today().date():
        return False 
    if expense_category not in helper.getSpendCategories():
        return False
    if helper.validate_entered_amount(expense_amount) == 0:
        return False 
    return True 

@add_bp.route('/add_single', methods=['POST'])
def add_single():
    """
    Add a single expense record. 
    
    Request JSON format:
    {
        "user_id" : "864914211",
        "amount" : "25.0",
        "date" : "2023-05-17",
        "category" : "Groceries",
        "currency" : "$"
    }

    Response  JSON format: 
    {
       "Expense record created succesfully"
    }
    """
    data = request.get_json()
    chat_id = data['user_id']
    expense_date = data['date']
    expense_category = data['category']
    expense_amount = data['amount']
    expense_currency = str(data['currency'])

    if not validate_add_request(chat_id, expense_date, expense_amount, expense_category):
        return jsonify({'error': 'Bad Request'}), 400
    

    date_str, category_str, amount_str = (
        expense_date,
        str(expense_category),
        str(expense_amount),
    )
    # get all user data 
    user_list = helper.read_json()
    if user_list is None :
        user_list.append("864914211") #Placeholder value
    # add new json for new user
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = {"data": [], "budget": {"overall": "0", "category": None}}
    record = "{},{},{}, {}".format(date_str, category_str, amount_str, expense_currency)
    # write data 
    user_list[str(chat_id)]["data"].append(record)
    helper.write_json(user_list)
    return jsonify({'message': 'Expense record created successfully'}), 200
    
