import json
from dotenv import load_dotenv, find_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
APP_SECRET = os.getenv("APP_SECRET")
APP_ID = os.getenv("APP_ID")

print(ACCESS_TOKEN)
print(RECIPIENT_WAID)
print(PHONE_NUMBER_ID)
print(VERSION)
print(APP_ID)
print(APP_SECRET)
if not all([ACCESS_TOKEN, RECIPIENT_WAID, PHONE_NUMBER_ID, VERSION, APP_ID]):
    raise ValueError("One or more environment variables are missing or undefined.")
# --------------------------------------------------------------
# Send a template WhatsApp message
# --------------------------------------------------------------

def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    # https://graph.facebook.com/860599774051206_4548643168486465/comments?access_token=APP_ID|APP_SECRET
    # https://graph.facebook.com/v5.0/me/adaccounts?access_token=EAA3vjE6nslIBO741vAowAx3WLfglQVoNFpEOh47Vco8ZANMMN7fxQat5ZC0uBR3PEAe1tpy54QVNOiuNyPvS6s0iOHoXzZAU1wlVTZAA9aul41PJzMWzVP9AuS6Pks64jffVsuSA1AAncVMOYlDZAP5mYGZCDtxdNTMGwHu4cwYB6ZBZCZC0jmExRnvxTTRKOiFvr4FpduHszM1mFjCAnmAs0W2LuXqeUJRjR0tYZBqd8ZD
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Call the function

# --------------------------------------------------------------
# Send a custom text WhatsApp messageresponse = send_whatsapp_message()
response = send_whatsapp_message()
print(response.status_code)
print(response.json())

# --------------------------------------------------------------

# NOTE: First reply to the message from the user in WhatsApp!


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Hello, This is a test message by dishu. \n Thank you"
)

response = send_message(data)

# --------------------------------------------------------------
# Send a custom text WhatsApp message asynchronously
# --------------------------------------------------------------


# Does not work with Jupyter!
async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = "https://graph.facebook.com" + f"/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Hello, this is a test message."
)

loop = asyncio.get_event_loop()
loop.run_until_complete(send_message(data))
loop.close()