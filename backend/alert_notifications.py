import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz

# Email configuration
GMAIL_USER = "your.email@gmail.com"  # Your Gmail address
# Generate an App Password: Google Account > Security > 2-Step Verification > App Passwords
GMAIL_APP_PASSWORD = "your_app_password"  # Gmail App Password (NOT your regular password)

# List of ranger email addresses to notify
RANGER_EMAILS = [
    # Add ranger email addresses here
    # "ranger1@example.com",
    # "ranger2@example.com"
]

def send_email_alert(email, detection_type, image_url=None, location=None):
    """
    Send email alert to ranger.
    
    Args:
        email (str): Ranger's email address
        detection_type (str): Type of detection (poacher or endangered species)
        image_url (str, optional): URL of the detected image
        location (dict, optional): Dictionary containing lat and lng coordinates
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = email
        msg['Subject'] = f"🚨 WildGuard Alert: {detection_type.replace('_', ' ').title()}"
        
        # Format the alert message
        montreal_tz = pytz.timezone('America/Montreal')
        current_time = datetime.now(montreal_tz).strftime("%Y-%m-%d %I:%M:%S %p %Z")
        
        body = f"""
        <html>
        <body>
        <h2>🚨 WildGuard Alert</h2>
        <p><strong>Detection:</strong> {detection_type.replace('_', ' ').title()}</p>
        <p><strong>Time:</strong> {current_time}</p>
        """
        
        if location:
            maps_url = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
            body += f"""
            <p><strong>Location:</strong></p>
            <ul>
                <li>Latitude: {location['lat']}</li>
                <li>Longitude: {location['lng']}</li>
                <li><a href="{maps_url}">View on Google Maps</a></li>
            </ul>
            """
            
        if image_url:
            body += f"""
            <p><strong>Detection Image:</strong></p>
            <p><a href="{image_url}">View Image</a></p>
            """
            
        body += """
        <p>Please take appropriate action immediately.</p>
        <hr>
        <em>This is an automated alert from the WildGuard system.</em>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
            
        print(f"Alert email sent to {email}")
        
    except Exception as e:
        print(f"Error sending email to {email}: {e}")

def notify_all_rangers(detection_type, image_url=None, location=None):
    """
    Send email alerts to all rangers.
    
    Args:
        detection_type (str): Type of detection (e.g., "poacher", "endangered_species")
        image_url (str, optional): URL of the detected image
        location (dict, optional): Dictionary containing lat and lng coordinates
    """
    if not RANGER_EMAILS:
        print("No ranger emails configured. Add emails to RANGER_EMAILS list.")
        return
        
    for email in RANGER_EMAILS:
        send_email_alert(email, detection_type, image_url, location)

print("""
Email Alert System Configuration:
1. Add your Gmail address as GMAIL_USER
2. Generate an App Password:
   - Go to your Google Account
   - Security > 2-Step Verification > App Passwords
   - Select 'Mail' and your device
   - Copy the generated password
3. Add the App Password as GMAIL_APP_PASSWORD
4. Add ranger email addresses to RANGER_EMAILS list

Note: This service is completely free and reliable!
You can receive alerts on any device with email access.
""")