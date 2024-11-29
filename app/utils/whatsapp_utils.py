# Store the current promptId of the users whose profile is being setup
# Once done, delete the entry from this list
#  It is a dictionary with key as wa_id and value as a new dictionary with key as prompt_id and value as the current prompt ID
# And a temp userInput dictionary to store the user input data
#  Example : {
#     "wa_id": {
#         "prompt_id": 1
#          "UserInput": {More user input data here}
#     }
# TODO(@dishukataria): This should be stored in a database or cache for persistence
import copy
from sqlite3 import OperationalError
import time
from typing import List

from sqlalchemy import desc

from app.databases.prompt import PromptData

initial_users_setup = {}

from flask import make_response, jsonify, current_app
from app.databases.reply_list import get_list_name_by_id,get_id_by_name,get_list_desc_by_id,get_available_quantity,edit_avalable_quantity
from app.databases.menu import fetch_active_menu_id
from app.dtos.dtos import SummaryDTO,PreviousOrderDTO

from app.databases.user_profile import UserProfile, check_user_exists, create_user_profile
from app.utils.prompt_utils import fetch_prompt, get_next_prompt, process_current_prompt, send_prompt
from app.databases.db_init import db
from app.databases.orders import save_order,Orders
from app.databases.order_items import save_order_item,OrderItems

from colorama import Fore, Back, Style

import requests
import logging

temp_item:str=""
summary_dtos:List[SummaryDTO]=[]
total_bill:float=0.0
flag_quantity:bool=0
item_available_quantity:int

previous_order_dto:List[PreviousOrderDTO]=[]


def add_summary_dto(item_name:str, quantity:int,item_desc:float) -> None:
    global total_bill
    
    item_total=quantity*float(item_desc)
    total_bill=total_bill+float(item_total)
    new_quantity=get_available_quantity(item_name=item_name)-quantity
    edit_avalable_quantity(item_name=item_name,new_quantity=new_quantity)
    for dto in summary_dtos:
        if dto.order_item == item_name:
            dto.quantity+=quantity
            dto.bill_amount+=item_total
            return
    # print(total_bill)
    summary_dtos.append(SummaryDTO(order_item=temp_item, quantity=quantity,bill_amount=item_total))


def add_order_to_the_db(wa_id,summary_dtos,total_bill):
    user=UserProfile.query.filter_by(user_phone_number=wa_id).first()
    save_order(user.id,total_bill)
    last_order = Orders.query.filter_by(ordered_by=user.id).order_by(desc(Orders.order_id)).first()
    order_id=last_order.order_id
    for dto in summary_dtos:
        item_id=get_id_by_name(dto.order_item)
        save_order_item(order_id,item_id,int(dto.quantity),float(dto.bill_amount))

def edit_order(summary_dtos,item_name,quantity):
    global total_bill
    for dto in summary_dtos:
        if dto.order_item == item_name:
            one_item=dto.bill_amount/dto.quantity
            new_quantity=get_available_quantity(item_name=item_name)+int(dto.quantity)-int(quantity)
            edit_avalable_quantity(item_name=item_name,new_quantity=new_quantity)
            dto.quantity=int(quantity)
            total_bill-=dto.bill_amount
            dto.bill_amount=float(one_item)*dto.quantity
            total_bill+=dto.bill_amount
    # summary_dtos.append(SummaryDTO(order_item=temp_item, quantity=quantity))

def fetch_previous_orders_from_db(wa_id):
    user=UserProfile.query.filter_by(user_phone_number=wa_id).first()
    if user is None:
        raise ValueError("User not found")
    all_orders_by_user=Orders.query.filter_by(ordered_by=user.id).all()
    for orders in all_orders_by_user:
        if (orders.completed == "yes"):
            items=OrderItems.query.filter_by(order_id=orders.order_id).all()
            previous_order_list:List[SummaryDTO]=[]
            for item in items:
                item_name=get_list_name_by_id(item.item_id) 
                if(check_active_menu_and_available_quantity(item_name,item.item_id,item.quantity)):
                    item_quantity=item.quantity
                    item_bill_amount=item.bill_amount
                    previous_order_list.append(SummaryDTO(item_name,item_quantity,item_bill_amount))
            if previous_order_list:
                previous_order_dto.append(PreviousOrderDTO(previous_order_list,orders.created_at,orders.grand_total))
    # print("All previous orders:", previous_order_dto)
                
def check_active_menu_and_available_quantity(item_name,item_id,item_quantity):
    prompt=PromptData.query.filter(PromptData.prompt_data_id==7).first()
    list_id_as_ints = [int(id) for id in prompt.list_id.split(',')]
    if(item_quantity<=get_available_quantity(item_name=item_name) and (item_id in list_id_as_ints) ):return True
    return False


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }
    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"})
    except requests.RequestException as e:
        logging.error(f"Request failed due to: {e.response.text}")
        return make_response(jsonify({"status": "error", "message": "Failed to send message"}), 500)
    else:
        logging.info(f"Message sent successfully. Response: {response.text}")
        return make_response(jsonify({"status": "success", "message": "Message sent"}), 200)

def process_whatsapp_message(message):
    """
    Process an incoming WhatsApp message.
    
    This function will handle the incoming WhatsApp message, check the user status, 
    and route to the appropriate prompt flow.
    """
    global summary_dtos
    global previous_order_dto
    global temp_item
    global temp_item_desc
    global total_bill
    global flag_quantity
    global item_available_quantity
    try:
        wa_id = message['entry'][0]['changes'][0]['value']['messages'][0]['from']  # Get sender's WhatsApp ID
    except KeyError as e:
        logging.error(f"Error extracting WhatsApp ID: {str(e)}")
        return
    # Initialize incoming_message for logging purposes
    incoming_message = None

    # Check if the message is interactive (button/list selection) or text message
    try:
        if 'interactive' in message['entry'][0]['changes'][0]['value']['messages'][0]:
            # Extract option or list selection from interactive message
            interactive_type = message['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['type']
            if interactive_type == 'button_reply':
                selected_option_id = message['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply']['id']
                incoming_message = f"Button reply with ID: {selected_option_id}"  # For logging
            elif interactive_type == 'list_reply':
                selected_option_id = message['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply']['id']
                incoming_message = f"List reply with ID: {selected_option_id}"  # For logging
            else:
                logging.error(f"Unknown interactive type: {interactive_type}")
                return
        else:
            # Handle standard text messages
            incoming_message = message['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            selected_option_id = None  # No option selected in a plain text message
    except KeyError as e:
        logging.error(f"Error processing message: {str(e)}")
        return

    # Log received message for debugging
    logging.info(f"Received message from {wa_id}: {incoming_message}")
    print(Back.GREEN+ f"Incoming message: {incoming_message}" + Style.RESET_ALL)
    print(db.session.query(UserProfile).all())
    # Step 1: Check if the user already exists in the system
    user = check_user_exists(wa_id)
    if not user:
        logging.info(f"User {wa_id} not found. Creating a new user profile.")
        user = create_user_profile(wa_id)

        # Send a welcome message or the first prompt
        first_prompt = fetch_prompt(1)  # Assuming prompt 1 is the starting prompt
        input = send_prompt(wa_id, first_prompt)
        send_message(input)
        initial_users_setup[wa_id] = {"prompt_id": 1}
    else:
        # Step 2: If user exists, determine the current prompt they are on
        logging.info(f"User {wa_id} exists. Fetching current prompt.")
        # You would need a way to track what prompt the user is on
        # Store in a dictionary initial_users_setup with key as wa_id and value as the current prompt ID
        current_prompt_id = initial_users_setup.get(wa_id, {}).get("prompt_id", 5)
        logging.info(f"Current prompt for user {wa_id}: {current_prompt_id}")
        process_current_prompt(wa_id, current_prompt_id, incoming_message)
        
        # Step 3: Fetch the next prompt based on their response
        next_prompt_id = get_next_prompt(current_prompt_id, selected_option_id)
        print(Back.GREEN + f"Current Prompt id: {current_prompt_id}, Next Prompt id: {next_prompt_id}, OP id: {selected_option_id}" + Style.RESET_ALL)

        # Populate summary variable
        if current_prompt_id is 7:
            item_id=int(incoming_message.split()[-1])
            item_name=get_list_name_by_id(item_id)
            item_desc=get_list_desc_by_id(item_id)
            temp_item=copy.deepcopy(item_name)
            temp_item_desc=copy.deepcopy(item_desc)

        elif current_prompt_id is 8:
            quantity=int(incoming_message)
            item_available_quantity=get_available_quantity(temp_item)
            if quantity<=item_available_quantity:
                flag_quantity=1
                add_summary_dto(item_name=temp_item, quantity=quantity,item_desc=temp_item_desc)
             
        elif current_prompt_id is 10:
            add_order_to_the_db(wa_id=wa_id,summary_dtos=summary_dtos,total_bill=total_bill)
            
        
        elif int(current_prompt_id) == 6 and int (selected_option_id)==3:
            fetch_previous_orders_from_db(wa_id=wa_id)
            for idx, order in enumerate(previous_order_dto):
            # Print each PreviousOrderDTO in green background
                print(Back.GREEN + f"Order {idx + 1}: {order}" + Style.RESET_ALL)
            next_prompt_id=15
        
        elif int(current_prompt_id) == 13:
            temp_item=incoming_message

        elif int(current_prompt_id) == 14:
            edit_order(summary_dtos=summary_dtos,item_name=temp_item,quantity=incoming_message)

        elif int(current_prompt_id)==15:
            # particular_number=(int)incoming_message
            five_last_order=previous_order_dto[-5:]
            particular_order=five_last_order[int(incoming_message)-1]
            # print(particular_order.summary_dtos)
            total_bill=particular_order.grand_total
            add_order_to_the_db(wa_id=wa_id,summary_dtos=particular_order.summary_dtos,total_bill=total_bill)
            summary_dtos=particular_order.summary_dtos
            # print(summary_dtos)

        if next_prompt_id:
            logging.info(f"Fetching next prompt ID {next_prompt_id} for user {wa_id}.")
            next_prompt = fetch_prompt(next_prompt_id)
            
            input = send_prompt(wa_id, next_prompt)
            if current_prompt_id is 8:
                if flag_quantity==1:
                    summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos)
                    summary += f"\nGlobal Total: ₹{total_bill:.2f}"
                    # input["interactive"]["body"]["text"]=f'\n {summary} \n {input["interactive"]["body"]["text"]}'
                    send_message({"messaging_product": "whatsapp", 
                            "recipient_type" : "individual", 
                            "to": f"+{wa_id}", 
                            "type": "text",
                            "text": {"body": f"Here's your order summary\n {summary} ","preview_url": False}})
                else:
                    send_message({"messaging_product": "whatsapp", 
                            "recipient_type" : "individual", 
                            "to": f"+{wa_id}", 
                            "type": "text",
                            "text": {"body": f"Available Quantity of {temp_item} is {item_available_quantity}\n Order accordingly","preview_url": False}})
                    summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos)
                    summary += f"\nGlobal Total: ₹{total_bill:.2f}"
                    send_message({"messaging_product": "whatsapp", 
                            "recipient_type" : "individual", 
                            "to": f"+{wa_id}", 
                            "type": "text",
                            "text": {"body": f"Here's your order summary\n {summary} ","preview_url": False}})
                flag_quantity=0


            elif int(current_prompt_id) == 9 and int (selected_option_id)==6:
                # summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos) + "\n"
                summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos)
                summary += f"\nGlobal Total: ₹{total_bill:.2f}"
                send_message({"messaging_product": "whatsapp", 
                          "recipient_type" : "individual", 
                          "to": f"+{wa_id}", 
                          "type": "text",
                          "text": {"body": f"{summary} ","preview_url": False}})
            
            elif int(current_prompt_id) == 10 and int (selected_option_id)==6:
                # summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos) + "\n"
                summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos)
                summary += f"\nGlobal Total: ₹{total_bill:.2f}"
                send_message({"messaging_product": "whatsapp", 
                          "recipient_type" : "individual", 
                          "to": f"+{wa_id}", 
                          "type": "text",
                          "text": {"body": f"{summary} ","preview_url": False}})
                
            elif int(current_prompt_id) == 6 and int (selected_option_id)==3:
                # previous_order = "\n".join(str(previous_order) for previous_order in previous_order_dto) + "\n"
                # previous_order = "\n".join(f"{idx + 1}. {order}" for idx, order in enumerate(previous_order_dto)) + "\n"
                recent_orders = previous_order_dto[-5:]
                previous_order = "\n".join(f"{idx + 1}. {order}" for idx, order in enumerate(recent_orders)) + "\n"

                # input["interactive"]["body"]["text"]=f'\n {summary} \n {input["interactive"]["body"]["text"]}'
                send_message({"messaging_product": "whatsapp", 
                          "recipient_type" : "individual", 
                          "to": f"+{wa_id}", 
                          "type": "text",
                          "text": {"body": f" Here's your previous orders:\n{previous_order} ","preview_url": False}})
                next_prompt_id=15

            elif current_prompt_id is 14:
                # summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos) + "\n"
                summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos)
                summary += f"\nGlobal Total: ₹{total_bill:.2f}"
                # input["interactive"]["body"]["text"]=f'\n {summary} \n {input["interactive"]["body"]["text"]}'
                send_message({"messaging_product": "whatsapp", 
                          "recipient_type" : "individual", 
                          "to": f"+{wa_id}", 
                          "type": "text",
                          "text": {"body": f"Here's your order summary\n {summary} ","preview_url": False}})
                
            print(Back.GREEN + f"Input: {input}" + Style.RESET_ALL)
            send_message(input)
            # Update the user's current prompt to the next prompt
            initial_users_setup[wa_id] = {"prompt_id": next_prompt_id, "UserInput":  initial_users_setup.get(wa_id, {}).get("UserInput", {})}

            
        else:
            # End of the flow
            # summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos) + "\n"
            summary = "\n".join(str(order_item_detail) for order_item_detail in summary_dtos)
            summary += f"\nGlobal Total: ₹{total_bill:.2f}"
            summary_dtos.clear()
            previous_order_dto.clear()
            total_bill=0
            logging.info(f"End of flow for user {wa_id}.")
            message={"messaging_product": "whatsapp", 
                          "recipient_type" : "individual", 
                          "to": f"+{wa_id}", 
                          "type": "text",
                          "text": {"body": f"{summary} Thank you! Your profile setup is complete.","preview_url": False}}
            
            print(Back.GREEN + f"Current Prompt id: {current_prompt_id}, Next Prompt id: {next_prompt_id}, OP id: {selected_option_id}" + Style.RESET_ALL)
            
            if int(current_prompt_id) == 11 and int(selected_option_id) == 8:
                print(Back.GREEN + f"Hereeeeeeeeeeeeee" + Style.RESET_ALL)
                message={"messaging_product": "whatsapp", 
                          "recipient_type" : "individual", 
                          "to": f"+{wa_id}", 
                          "type": "text",
                          "text": {"body": f" Great! Order Placed\n Order Summary:\n{summary} \nPayment Status: COD.","preview_url": False}}
                
            send_message(message)
            # Reset current prompt id as 5 to restart chat flow for the same user to continue with the same profile
            initial_users_setup[wa_id] = {"prompt_id": 5}


            

def is_valid_whatsapp_message(message):
    """
    Validate whether the incoming message is a valid WhatsApp message.
    
    This could involve checking if the message contains the required fields or
    if the message originated from the WhatsApp API.
    """
    try:
        # Check if the necessary fields exist in the incoming message
        entry = message.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        # Check if this is a valid message with the necessary structure
        if value.get("messages"):
            return True
        return False
    except (KeyError, IndexError):
        # Log the error if the message structure is not as expected
        print("Invalid WhatsApp message format")
        return False