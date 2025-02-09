from twilio.rest import Client
from datetime import datetime
import pytz

# Twilio credentials
TWILIO_ACCOUNT_SID = "AC8002b8621c0bb9b84f1795936aeb2f35"
TWILIO_AUTH_TOKEN = "9d86b985c0933a08a8c695e9523b3e39"

# Twilio phone number
TWILIO_PHONE_NUMBER = "+18153359537"

# Ranger phone numbers
RANGER_PHONE_NUMBERS = [
    "+15145814055",
    "+14383579553"
]

# Initialize Twilio client
client = None

def initialize_twilio():
    """Initialize Twilio client with credentials"""
    global client
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("Successfully connected to Twilio")
        return True
    except Exception as e:
        print(f"Error initializing Twilio: {e}")
        print("SMS notifications will be disabled")
        return False

def send_sms_alert(phone_number, detection_type, image_url=None, location=None):
    """
    Send SMS alert using Twilio.
    
    Args:
        phone_number (str): Phone number to send alert to
        detection_type (str): Type of detection (poacher or endangered species)
        image_url (str, optional): URL of the detected image
        location (dict, optional): Dictionary containing lat and lng coordinates
    """
    if not client:
        print("Twilio not initialized. SMS will not be sent.")
        return

    try:
        # Format the message
        montreal_tz = pytz.timezone('America/Montreal')
        current_time = datetime.now(montreal_tz).strftime("%I:%M:%S %p %Z")
        
        # Create alert message
        alert_type = detection_type.replace('_', ' ').title()
        message = f"🚨 WildGuard Alert!\n"
        message += f"Type: {alert_type}\n"
        message += f"Time: {current_time}"
        
        if location:
            maps_url = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
            message += f"\n\nLocation: {maps_url}"
        
        if image_url:
            message += f"\n\nImage: {image_url}"

        if alert_type == "Poacher":
            message += "\n\nPlease take immediate action!"
        else:
            message += f"\n\nFiche technique: https://wikipedia.org/wiki/{alert_type}"
        
        # Send SMS using Twilio
        sms = client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        
        print(f"Alert SMS sent to {phone_number} (Message SID: {sms.sid})")
        
    except Exception as e:
        print(f"Error sending SMS to {phone_number}: {e}")

def notify_all_rangers(detection_type, image_url=None, location=None):
    """
    Send SMS alerts to all configured ranger numbers.
    
    Args:
        detection_type (str): Type of detection (e.g., "poacher", "endangered_species")
        image_url (str, optional): URL of the detected image
        location (dict, optional): Dictionary containing lat and lng coordinates
    """
    if not RANGER_PHONE_NUMBERS:
        print("No ranger phone numbers configured.")
        return
        
    for phone_number in RANGER_PHONE_NUMBERS:
        send_sms_alert(phone_number, detection_type, image_url, location)

# Initialize Twilio when module is imported
initialize_twilio()