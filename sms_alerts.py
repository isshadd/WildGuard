# import requests
# import json

# # FastSMS API configuration
# API_URL = "https://www.fast2sms.com/dev/bulk"
# # Get your free API key from https://www.fast2sms.com/
# API_KEY = "your_api_key_here"

# # List of ranger phone numbers to notify
# RANGER_PHONE_NUMBERS = [
#     # Add phone numbers without country code (e.g., "9876543210")
# ]

# def send_sms_alert(phone_number, detection_type, location=None):
#     """
#     Send SMS alert using Fast2SMS API (free service).
    
#     Args:
#         phone_number (str): Phone number without country code
#         detection_type (str): Type of detection (poacher or endangered species)
#         location (dict, optional): Dictionary containing lat and lng coordinates
#     """
#     # Format the message
#     alert_type = detection_type.replace('_', ' ').title()
#     message = f"WildGuard Alert: {alert_type} detected!"
    
#     if location:
#         maps_url = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
#         message += f" Location: {maps_url}"

#     try:
#         headers = {
#             "authorization": API_KEY,
#             "Content-Type": "application/json"
#         }
        
#         payload = {
#             "route": "v3",
#             "sender_id": "TXTIND",
#             "message": message,
#             "language": "english",
#             "flash": 0,
#             "numbers": phone_number
#         }
        
#         response = requests.post(
#             API_URL,
#             headers=headers,
#             data=json.dumps(payload)
#         )
        
#         if response.status_code == 200:
#             result = response.json()
#             if result.get('return'):
#                 print(f"Alert SMS sent to {phone_number}")
#             else:
#                 print(f"Failed to send SMS: {result.get('message')}")
#         else:
#             print(f"API request failed with status code: {response.status_code}")
            
#     except Exception as e:
#         print(f"Error sending SMS: {e}")

# def notify_all_rangers(detection_type, location=None):
#     """
#     Send SMS alerts to all rangers.
    
#     Args:
#         detection_type (str): Type of detection (e.g., "poacher", "endangered_species")
#         location (dict, optional): Dictionary containing lat and lng coordinates
#     """
#     if not RANGER_PHONE_NUMBERS:
#         print("No ranger phone numbers configured. Add numbers to RANGER_PHONE_NUMBERS.")
#         return
        
#     for phone_number in RANGER_PHONE_NUMBERS:
#         send_sms_alert(phone_number, detection_type, location)

# print("FastSMS Alert System Configuration:")
# print("1. Sign up at https://www.fast2sms.com/")
# print("2. Get your free API key from the dashboard")
# print("3. Add ranger phone numbers to RANGER_PHONE_NUMBERS")
# print("Note: This service is completely free for development/testing!")