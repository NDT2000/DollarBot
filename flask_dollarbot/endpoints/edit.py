from flask import Blueprint, request, jsonify
import  endpoints.helper as helper
from datetime import datetime

# Create a Blueprint for editing expenses
edit_bp = Blueprint('edit', __name__)
MAX_AMOUNT_LIMIT = 1000000  # Example threshold for large amounts
@edit_bp.route('/edit_cost', methods=['POST'])
def edit_cost():
    """
    Edit the cost of an existing expense.

    Request JSON format:
    {
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_cost": "55.0"
    }

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    user_id = data.get('user_id')
    selected_data = data.get('selected_data')
    new_cost = data.get('new_cost')
    
    # Basic input validation for user_id, selected_data, and new_cost
    if not user_id or not selected_data or not new_cost:
        return jsonify({'error': 'Invalid input'}), 400

    # Validate the amount and ensure it doesn't exceed a predefined limit
    try:
        if float(new_cost) > MAX_AMOUNT_LIMIT:
            return jsonify({'error': 'Amount exceeds limit'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    if helper.validate_entered_amount(new_cost) == 0:
        return jsonify({'error': 'Invalid amount'}), 400

    # Fetch user data and validate user existence
    user_list = helper.read_json()
    data_edit = helper.getUserHistory(user_id)
    if data_edit is None:
        return jsonify({"error": "user is missing or invalid"}), 400

    # Extract and validate date format
    try:
        selected_date = selected_data[0].split("=")[1]
        datetime.strptime(selected_date, helper.getDateFormat())
    except (IndexError, ValueError):
        return jsonify({'error': 'Invalid date format'}), 400

    # Extract category and amount
    selected_category = selected_data[1].split("=")[1]
    selected_amount = selected_data[2].split("=")[1]
    
    category_found = False  # Track if category is found

    for i in range(len(data_edit)):
        user_data = data_edit[i].split(",")
        selected_currency = user_data[3] if len(user_data) >= 4 else "dollar"

        if (
            user_data[0] == selected_date and
            user_data[1] == selected_category and
            user_data[2] == selected_amount
        ):
            data_edit[i] = f"{selected_date},{selected_category},{new_cost},{selected_currency}"
            category_found = True  # Mark category as found
            break

    if not category_found:
        return jsonify({'error': 'Category not found'}), 404

    # Update user data and write changes
    user_list[str(user_id)]["data"] = data_edit
    helper.write_json(user_list)

    return jsonify({'message': 'Cost updated successfully'}), 200


@edit_bp.route('/edit_date', methods=['POST'])
def edit_date():
    """
    Edit the date of an existing expense.

    Request JSON format:
    {
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Transport",
            "Amount=50.0"
        ],
        "new_date": "18-May-2023"
    }

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    user_id = data.get('user_id')
    selected_data = data.get('selected_data')
    new_date = data.get('new_date')

    if not user_id or not selected_data or not new_date:
        return jsonify({'error': 'Invalid input'}), 400

    user_list = helper.read_json()
    chat_id = user_id
    data_edit = helper.getUserHistory(chat_id)

    for i in range(len(data_edit)):
        user_data = data_edit[i].split(",")
        selected_date = selected_data[0].split("=")[1]
        selected_category = selected_data[1].split("=")[1]
        selected_amount = selected_data[2].split("=")[1]
        if len(user_data)>=4:
            selected_currency = user_data[3]
        else:
            selected_currency = "dollar"

        if (
            user_data[0] == selected_date and
            user_data[1] == selected_category and
            user_data[2] == selected_amount
        ):
            new_date_formatted = datetime.strptime(new_date, '%Y-%m-%d').date()
            data_edit[i] = f"{new_date_formatted},{selected_category},{selected_amount},{selected_currency}"
            break

    user_list[str(chat_id)]["data"] = data_edit
    helper.write_json(user_list)

    return jsonify({'message': 'Date updated successfully'}), 200


@edit_bp.route('/edit_category', methods=['POST'])
def edit_category():
    """
    Edit the category of an existing expense.

    Request JSON format:
    {
        "user_id": "864914211",
        "selected_data": [
            "Date=17-May-2023",
            "Category=Groceries",
            "Amount=50.0"
        ],
        "new_category": "Travel"
    }

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    user_id = data.get('user_id')
    selected_data = data.get('selected_data')
    new_category = data.get('new_category')

    if not user_id or not selected_data or not new_category:
        return jsonify({'error': 'Invalid input'}), 400

    user_list = helper.read_json()
    chat_id = user_id
    data_edit = helper.getUserHistory(chat_id)

    for i in range(len(data_edit)):
        user_data = data_edit[i].split(",")
        selected_date = selected_data[0].split("=")[1]
        selected_category = selected_data[1].split("=")[1]
        selected_amount = selected_data[2].split("=")[1]
        if len(user_data)>=4:
            selected_currency = user_data[3]
        else:
            selected_currency = "dollar"

        if (
            user_data[0] == selected_date and
            user_data[1] == selected_category and
            user_data[2] == selected_amount
        ):
            data_edit[i] = f"{selected_date},{new_category},{selected_amount},{selected_currency}"
            break

    user_list[str(chat_id)]["data"] = data_edit
    helper.write_json(user_list)

    return jsonify({'message': 'Category updated successfully'}), 200


# @edit_bp.route('/history', methods=['GET'])
# def get_user_history():
#     """
#     Retrieve the expense history for a user.

#     Request URL: /edit/history?user_id=864914211

#     Returns:
#         JSON response with user expense history.
#     """
#     user_id = request.args.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'User ID is required'}), 400

#     user_history = helper.getUserHistory(user_id)
#     if not user_history:
#         return jsonify({'message': 'No recorded expenses found'}), 404

#     expenses = []
#     for c in user_history:
#         expense_data = c.split(",")
#         expenses.append({
#             "date": expense_data[0],
#             "category": expense_data[1],
#             "amount": float(expense_data[2])
#         })

#     return jsonify({'expenses': expenses}), 200
