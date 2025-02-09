# from twilio.rest import Client
# import os

# # Twilio credentials (replace these with your actual credentials)
# TWILIO_ACCOUNT_SID = "your_account_sid"
# TWILIO_AUTH_TOKEN = "your_auth_token"
# TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

# # Initialize Twilio client
# client = None

# def initialize_twilio():
#     """Initialize Twilio client with credentials"""
#     global client
#     try:
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#         print("Successfully connected to Twilio")
#     except Exception as e:
#         print(f"Error initializing Twilio: {e}")
#         print("SMS notifications will be disabled")

# def send_sms_alert(phone_number, detection_type, location=None):
#     """
#     Send SMS alert to specified phone number.
    
#     Args:
#         phone_number (str): Recipient's phone number (format: +1234567890)
#         detection_type (str): Type of detection (e.g., "poacher", "endangered_species")
#         location (dict, optional): Dictionary containing lat and lng coordinates
#     """
#     if not client:
#         print("Twilio not initialized. SMS will not be sent.")
#         return
    
#     try:
#         # Format the message
#         message = f"🚨 WildGuard Alert: {detection_type.replace('_', ' ').title()} detected!"
        
#         if location:
#             message += f"\nLocation: {location['lat']}, {location['lng']}"
#             # Add Google Maps link
#             maps_url = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
#             message += f"\nMap: {maps_url}"
        
#         # Send the SMS
#         message = client.messages.create(
#             body=message,
#             from_=TWILIO_PHONE_NUMBER,
#             to=phone_number
#         )
        
#         print(f"SMS alert sent successfully! SID: {message.sid}")
        
#     except Exception as e:
#         print(f"Error sending SMS alert: {e}")

# # List of ranger phone numbers to notify (replace with actual numbers)
# RANGER_PHONE_NUMBERS = [
#     "+1234567890",  # Replace with actual phone numbers
#     # Add more ranger phone numbers here
# ]

# def notify_all_rangers(detection_type, location=None):
#     """
#     Send SMS alerts to all rangers.
    
#     Args:
#         detection_type (str): Type of detection (e.g., "poacher", "endangered_species")
#         location (dict, optional): Dictionary containing lat and lng coordinates
#     """
#     for phone_number in RANGER_PHONE_NUMBERS:
#         send_sms_alert(phone_number, detection_type, location)

# # Initialize Twilio when module is imported
# initialize_twilio()