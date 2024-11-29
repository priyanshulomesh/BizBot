from app.databases.heading_desc import HeadingDesc
from app.databases.prompt import PromptData, PromptFlow
from app.databases.reply_option import  create_reply_options
from app.databases.db_init import db
from colorama import Fore, Back, Style

import logging

from app.databases.user_profile import UserProfile
from app.databases.user_input import UserInput
from app.databases.user_input import save_user_input
from .whatsapp_utils import initial_users_setup
from app.databases import reply_list
from app.databases.menu import Menu
from app.databases.menu_reply_association import MenuReplyAssociation
# from app.databases import menu_reply_association
from app.databases.reply_list import create_list_items

# def create_list_items(list_ids):
#     menu_active = Menu.query.filter(Menu.active.is_(True)).first()
#     reply_list_ids = MenuReplyAssociation.query.filter(MenuReplyAssociation.menu_id == menu_active.menu_id).all()
#     # lists = ReplyList.query.filter(ReplyList.list_id.in_(list_ids.split(','))).all()
#     # print("\033[92mReply list IDs for active menu {}: {}\033[0m".format(reply_list_ids))
#     # return [{"id": l.list_id, "name": l.list_name, "desc": l.list_desc} for l in lists] 
#     list_ids = [reply_list_id[0] for reply_list_id in reply_list_ids]
#     lists = ReplyList.query.filter(ReplyList.list_id.in_(list_ids)).all()
#     return [
#         {
#             "id": l.list_id,
#             "name": l.list_name,
#             "desc": l.list_desc,
#         }
#         for l in lists
#     ]
# Function to fetch a prompt by its ID
def fetch_prompt(prompt_id):
    logging.info(f"Fetching prompt with ID {prompt_id}.")
    prompt_data = PromptData.query.filter_by(prompt_data_id=prompt_id).first()
    
    if not prompt_data:
        logging.warning(f"No prompt found with ID {prompt_id}.")
        return None
    
    heading = HeadingDesc.query.filter_by(header_id=prompt_data.header_id).first()
    logging.info(f"Found prompt heading: {heading.desc if heading else 'None'}")
    
    return {
        "heading": heading.desc if heading else None,
        "attachment_type": prompt_data.attachment_type,
        "option_ids": prompt_data.option_id,
        "list_ids": prompt_data.list_id
    }
def check_user_info_exists(user_profile):
    if UserInput.query.filter_by(user_profile_id=user_profile.id).first():
        return False
    return True

def process_current_prompt(wa_id : int, current_prompt_id: int, incoming_message : str):
    # Get current userProfile dict
    current_user = initial_users_setup.get(wa_id, {}).get("UserInput", {})
    match current_prompt_id:
        case 1:
            current_user["user_name"] = incoming_message
        case 2:
            current_user["address"] = incoming_message
        # case 3:
        #     current_user["pincode"] = incoming_message
        # case 4:
        #     current_user["city"] = incoming_message
        # case 5:
        #     current_user["state"] = incoming_message
    initial_users_setup[wa_id] = {"prompt_id": current_prompt_id, "UserInput": current_user}
    # Fetch the user's profile based on their phone number
    user_profile = UserProfile.query.filter_by(user_phone_number=wa_id).first()
    if(current_prompt_id == 2 and check_user_info_exists(user_profile=user_profile)):
        save_user_input(wa_id, current_user)
        del initial_users_setup[wa_id]

    else:
        #set curent promptid to 6
        current_prompt_id = 6
        send_prompt(wa_id, fetch_prompt(current_prompt_id))
    
def get_next_prompt(current_prompt_id, selected_option_id: int = None):
    # Fetch prompt flow based on selected option if available, otherwise fetch based on current prompt only
    if current_prompt_id is 7:
        selected_option_id=None
        
    if selected_option_id is not None:
        prompt_flow = PromptFlow.query.filter_by(current_prompt_id=current_prompt_id, option_id=selected_option_id).first()
    else:
        # This is for the case when there is no selected option (e.g., in list replies)
        prompt_flow = PromptFlow.query.filter_by(current_prompt_id=current_prompt_id).first()
    
    # Log the prompt flow object or lack of it
    if prompt_flow is None:
        logging.warning(f"No prompt flow found for current_prompt_id: {current_prompt_id} and selected_option_id: {selected_option_id}")
        return None

    # Safeguard the access to next_prompt_id and check for end of flow
    if not prompt_flow.is_end:
        logging.info(f"Next prompt ID: {prompt_flow.next_prompt_id}")
        return prompt_flow.next_prompt_id
    else:
        logging.info(f"End of flow reached at current_prompt_id: {current_prompt_id}")
    return None

# Function to handle sending the prompt based on its type
def send_prompt(wa_id, prompt_data):
    logging.info(f"Sending prompt to user {wa_id}. Prompt data {prompt_data}" )
# https://developers.facebook.com/docs/whatsapp/cloud-api/messages/text-messages
    if prompt_data['attachment_type'] == 'text':
       return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": wa_id,
            "type": "text",
            "text": {"body": prompt_data['heading']}
       }

# https://developers.facebook.com/docs/whatsapp/cloud-api/messages/interactive-reply-buttons-messages
    elif prompt_data['attachment_type'] == 'reply':
        options = create_reply_options(prompt_data['option_ids'])
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": wa_id,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": prompt_data['heading']},
                "action": {"buttons": options}
            }
         }

# https://developers.facebook.com/docs/whatsapp/cloud-api/messages/interactive-list-messages
    elif prompt_data['attachment_type'] == 'list':
        lists = create_list_items(prompt_data['list_ids'])
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": wa_id,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": prompt_data['heading']},
                "action": {
                    "button": "Select an option",
                    "sections": [{
                        "title": "Options",
                        "rows": [{"id": item['id'], "title": item['name'], "description": item['desc']} for item in lists]
                    }]
                }
            }
        }