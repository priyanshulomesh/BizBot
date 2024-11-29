from datetime import date
from operator import or_
from colorama import Back, Style
from flask import jsonify,request
from sqlalchemy import text

from app import create_app, db

from app.databases.menu_reply_association import MenuReplyAssociation
from app.databases.user_profile import UserProfile
from app.databases.user_input import UserInput
from app.databases.orders import Orders
from app.databases.order_items import OrderItems
from app.databases.reply_list import ReplyList
from app.databases.menu import Menu
from app.databases.prompt import PromptData 
from flask_cors import cross_origin

app = create_app()

@app.route('/')
def index():
    Menu.add_menu("Lunch","Lunch khao")
    Menu.add_menu("Dinner","Dinner kro")
    Menu.add_menu("Breakfast","breakfast")
    Menu.add_menu("Snacks","Nashta")

    Menu.add_item_to_menu
    return "Chatbot is running and database is connected!"

@app.route('/check_db') 
def check_db(): 
    try: 
    # Issue a simple query to check the connection 
        db.session.execute(text('SELECT 1'))
        return "Database connected successfully!" 
    except Exception as e: 
        return f"Error connecting to the database: {e}"

@app.route('/user_profiles_with_inputs', methods=['GET'])
def get_all_user_profiles_with_inputs():
    # Fetch all UserProfile entries
    user_profiles = UserProfile.query.all()

    # Construct response data
    response_data = []
    for profile in user_profiles:
        profile_data = {
            'id': profile.id,
            'user_phone_number': profile.user_phone_number,
            'created_at': profile.created_at,
            'user_inputs': [user_input.to_dict() for user_input in profile.user_inputs]
        }
        response_data.append(profile_data)
    
    return jsonify(response_data)

@app.route('/incomplete_orders', methods=['GET'])
def get_incomplete_orders():
    # Fetch all incomplete orders
    incomplete_orders = Orders.query.filter_by(completed="no").all()
    
    order_details = []
    
    for order in incomplete_orders:
        # Fetch associated OrderItems
        items = OrderItems.query.filter_by(order_id=order.order_id).all()
        
        order_items_list = []
        for item in items:
            # Fetch the item name from the ReplyList
            item_detail = ReplyList.query.filter_by(list_id=item.item_id).first()  # Adjust if your item_id references a different model
            item_name = item_detail.list_name if item_detail else "Unknown Item"  # Handle case where item is not found
            
            order_items_list.append({
                'item_id': item.item_id,
                'item_name': item_name,
                'quantity': item.quantity,
            })
        
        # Fetch user details
        user = UserProfile.query.get(order.ordered_by)
        
        # Fetch associated user input
        user_inputs = UserInput.query.filter_by(user_profile_id=user.id).all() if user else []
        
        user_input_list = []
        for user_input in user_inputs:
            user_input_list.append({
                'user_name': user_input.user_name,
                'gender': user_input.gender,
                'address': user_input.user_Address
            })

        formatted_created_at = order.created_at.strftime('%Y-%m-%d, %H:%M')
        # Prepare order details
        order_info = {
            'order_id': order.order_id,
            'ordered_by': user.user_phone_number if user else None,  # Get user phone number
            'created_at': formatted_created_at,
            'user_inputs': user_input_list,  # Add user input details
            'items': order_items_list,
            'grand_total': order.grand_total 
        }
        
        order_details.append(order_info)

    return jsonify(order_details)

@app.route('/complete_orders', methods=['GET'])
def get_complete_orders():
    # Fetch all incomplete orders
    # incomplete_orders = Orders.query.filter_by(completed="yes").all()
    incomplete_orders = Orders.query.filter(or_(Orders.completed == "yes", Orders.completed=="Cancel")).all()
    order_details = []
    
    for order in incomplete_orders:
        # Fetch associated OrderItems
        items = OrderItems.query.filter_by(order_id=order.order_id).all()
        
        order_items_list = []
        for item in items:
            # Fetch the item name from the ReplyList
            item_detail = ReplyList.query.filter_by(list_id=item.item_id).first()  # Adjust if your item_id references a different model
            item_name = item_detail.list_name if item_detail else "Unknown Item"  # Handle case where item is not found
            
            order_items_list.append({
                'item_id': item.item_id,
                'item_name': item_name,
                'quantity': item.quantity
            })
        
        # Fetch user details
        user = UserProfile.query.get(order.ordered_by)
        
        # Fetch associated user input
        user_inputs = UserInput.query.filter_by(user_profile_id=user.id).all() if user else []
        
        user_input_list = []
        for user_input in user_inputs:
            user_input_list.append({
                'user_name': user_input.user_name,
                'gender': user_input.gender,
                'address': user_input.user_Address
            })
        formatted_created_at = order.created_at.strftime('%Y-%m-%d, %H:%M')
        # Prepare order details
        order_info = {
            'order_id': order.order_id,
            'ordered_by': user.user_phone_number if user else None,  # Get user phone number
            'created_at': formatted_created_at,
            'user_inputs': user_input_list,  # Add user input details
            'items': order_items_list,
            'grand_total': order.grand_total,
            'order_status':order.completed
        }
        
        order_details.append(order_info)

    return jsonify(order_details)

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def toggle_order_status(order_id):
    # Fetch the order by ID
    order = Orders.query.get(order_id)
    
    # Check if order exists
    if order is None:
        return jsonify({'error': 'Order not found'}), 404

    # Check and update the status
    new_status = request.json.get("status")

    if new_status=="Delivered":
        if order.completed == "no":
            order.completed = "yes"
            db.session.commit()
            return jsonify({'message': 'Order status updated to yes', 'order_id': order_id}), 200
        else:
            return jsonify({'message': 'Order is already completed', 'order_id': order_id}), 200
        
    elif new_status=="Cancelled":
        order.completed="cancel"
        db.session.commit()
        return jsonify({'message': 'Order status updated to cancelled', 'order_id': order_id}), 200
    else:
        return jsonify({'error': 'Invalid status provided'}), 400


@app.route('/reply_lists', methods=['GET'])
def get_all_reply_lists():
    """
    
        Get all reply lists with their associated menu items.

        Sample api response
        [
            {
                "list_id": 1,
                "list_name": "Samosa",
                "list_desc": "Description for List 1",
                "menus": [
                    {
                        "menu_id": 1,
                        "menu_name": "Lunch Menu",
                        "menu_desc": "Menu for lunch items",
                        "active": true
                    },
                    {
                        "menu_id": 2,
                        "menu_name": "Dinner Menu",
                        "menu_desc": "Menu for dinner items",
                        "active": false
                    }
                ]
            },
            {
                "list_id": 2,
                "list_name": "Sample List 2",
                "list_desc": "Description for List 2",
                "menus": [
                    {
                        "menu_id": 3,
                        "menu_name": "Breakfast Menu",
                        "menu_desc": "Menu for breakfast items",
                        "active": false
                    }
                ]
            }
]

    
    """

    reply_lists = ReplyList.query.all()
    result = []

    for reply_list in reply_lists:
        reply_list_data = {
            'list_id': reply_list.list_id,
            'list_name': reply_list.list_name,
            'list_desc': reply_list.list_desc,
            'available_quantity': reply_list.available_quantity,
            'menus': [
                {
                    'menu_id': menu.menu.menu_id,
                    'menu_name': menu.menu.menu_name,
                    'menu_desc': menu.menu.menu_desc,
                    'active': menu.menu.active
                } for menu in reply_list.menus
            ]
        }
        result.append(reply_list_data)
    return jsonify(result), 200

@app.route('/menus', methods=['GET'])
def get_all_menus():
    """
        Get all menu items with their associated reply lists.


        [
            {
                "menu_id": 1,
                "menu_name": "Lunch Menu",
                "menu_desc": "Menu for lunch items",
                "active": true,
            },
            {
                "menu_id": 2,
                "menu_name": "Dinner Menu",
                "menu_desc": "Menu for dinner items",
                "active": false,
            }
        ]

    

    
    
    
    
    """
    
    menus = Menu.query.all()
    result = []

    for menu in menus:
        menu_data = {
            'menu_id': menu.menu_id,
            'menu_name': menu.menu_name,
            'menu_desc': menu.menu_desc,
            'active': menu.active,
        }
        result.append(menu_data)

    return jsonify(result), 200

@app.route('/menus/<int:menu_id>/activate', methods=['PUT'])
def update_active_menu(menu_id):
    """
    API Endpoint to activate a menu and deactivate all others.

    Sample Request:
    PUT /menus/1/activate
    {
        "menu_id": 1
    }

    Sample Response on Success:
    {
        "message": "Menu activated successfully",
        "menu_id": 1
    }

    Sample Response on Error (Menu not found):
    {
        "error": "Menu not found"
    }
    """
    try:
        # Call the static method from Menu model to set active menu
        Menu.set_active(menu_id)
        prompt=PromptData.query.filter(PromptData.prompt_data_id==7).first()
        menu_active = Menu.query.filter(Menu.active.is_(True)).first()
        reply_list_idss = db.session.query(MenuReplyAssociation.reply_list_id).filter(MenuReplyAssociation.menu_id == menu_active.menu_id).all()
        reply_list_ids = [str(row[0]) for row in reply_list_idss]  # Convert each ID to a string

        prompt.list_id = ",".join(reply_list_ids)
        db.session.commit()
        return jsonify({'message': 'Menu activated successfully', 'menu_id': menu_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/menus/<int:menu_id>/items', methods=['GET'])
def get_menu_items(menu_id):
    # Fetch items for the given menu
    reply_list = ReplyList.query.join(MenuReplyAssociation).filter_by(menu_id=menu_id).all()
    return jsonify([{'list_id': item.list_id, 'list_name': item.list_name, 'list_desc': item.list_desc, 'available_quantity' : item.available_quantity} for item in reply_list])

@app.route('/menus/<int:menu_id>/items', methods=['PUT'])
def update_menu_items(menu_id):
    data = request.json
    items = data.get('items', [])

    for item_data in items:
        list_id = item_data.get('list_id')
        list_name = item_data.get('list_name')
        list_desc = item_data.get('list_desc')
        available_quantity = item_data.get('available_quantity')

        if list_id:
            # Update existing item
            item = ReplyList.query.get(list_id)
            if item:
                item.list_name = list_name
                item.list_desc = list_desc
                item.available_quantity = available_quantity
        else:
            # Add new item
            new_item = ReplyList(list_name=list_name, list_desc=list_desc, available_quantity=available_quantity)
            db.session.add(new_item)
            db.session.flush()  # To get the ID of the new item
            # Create association between the menu and new item
            menu_association = MenuReplyAssociation(menu_id=menu_id, reply_list_id=new_item.list_id)
            db.session.add(menu_association)

    db.session.commit()
    return jsonify({'status': 'success'}), 200

@app.route('/overview', methods=['GET'])
def get_revenue():
    try:
        # Get today's date (local date)
        today = date.today()

        # Query for the grand_total of orders completed on today's date
        total_revenue = db.session.query(db.func.sum(Orders.grand_total)).filter(
            db.func.date(Orders.created_at) == today,
            Orders.completed == "yes"
        ).scalar()

        # If there are no completed orders today, set total_revenue to 0
        total_revenue = total_revenue or 0.0

        total_orders = db.session.query(Orders).filter(
            db.func.date(Orders.created_at) == today,
            Orders.completed == "yes"
        ).count()

        # Total unique customers who placed orders today
        total_customers = db.session.query(Orders.ordered_by).filter(
            db.func.date(Orders.created_at) == today,
            Orders.completed == "yes"
        ).distinct().count()

        # Construct and return the response JSON
        return jsonify({
            'date': today.strftime('%Y-%m-%d'),
            'totalRevenue': total_revenue,
            'totalOrders': total_orders,
            'totalCustomers': total_customers
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # TODO: Remove debug=True when deploying to production
    app.run(host="0.0.0.0", port=8000,debug=True,use_debugger=False, use_reloader=False)