import os
from datetime import datetime
import mimetypes
from supabase import create_client, Client
import pytz
import uuid
from twilio_notifications import notify_all_rangers

# Supabase configuration
SUPABASE_URL = "https://vtnrhbkqjorezqhiuogf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ0bnJoYmtxam9yZXpxaGl1b2dmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwNTE2NjgsImV4cCI6MjA1NDYyNzY2OH0.HSTDY_4ATr0-uHfVCUghu-46NxjUKRYprVINdKk4wUk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Montreal timezone
MONTREAL_TZ = pytz.timezone('America/Montreal')

def format_datetime_montreal(timestamp_str):
    """Convert UTC timestamp string to Montreal time string"""
    if not timestamp_str:
        return "unknown time"
    
    try:
        # Parse the UTC timestamp
        utc_dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Convert to Montreal time
        montreal_dt = utc_dt.astimezone(MONTREAL_TZ)
        
        # Format with timezone name
        return montreal_dt.strftime("%Y-%m-%d %I:%M:%S %p %Z")
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return timestamp_str

def initialize_storage():
    """
    Initialize storage bucket if it doesn't exist.
    For Supabase, buckets are created via dashboard, so this just validates connection.
    """
    try:
        # List buckets to verify connection
        supabase.storage.list_buckets()
        print("Successfully connected to Supabase storage")
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        print("Please ensure you've created the 'wildguard' bucket in Supabase Storage dashboard")
        raise

def get_content_type(file_path):
    """
    Get the content type of a file based on its extension.
    """
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or 'application/octet-stream'

def generate_unique_filename(original_filename):
    """Generate a unique filename with timestamp and UUID"""
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now(MONTREAL_TZ).strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{timestamp}_{unique_id}{ext}"

def upload_image(image_path, destination_folder="alerts"):
    """
    Upload an image to Supabase Storage and return its public URL.
    
    Args:
        image_path (str): Local path to the image file
        destination_folder (str): Folder in storage to upload to
        
    Returns:
        str: Public URL of the uploaded image
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    try:
        # Generate unique filename
        original_filename = os.path.basename(image_path)
        unique_filename = generate_unique_filename(original_filename)
        print(f"Uploading image as: {unique_filename}")
        
        # Read file content
        with open(image_path, "rb") as f:
            file_content = f.read()
        
        # Upload to Supabase Storage with minimal options
        result = supabase.storage.from_("wildguard").upload(
            path=unique_filename,
            file=file_content
        )
        
        # Get public URL
        public_url = supabase.storage.from_("wildguard").get_public_url(unique_filename)
        print(f"Successfully uploaded image: {public_url}")
        
        return public_url
    
    except Exception as e:
        print(f"Error uploading image: {e}")
        raise

def send_alert(image_path, detection_label, location=None):
    """
    Send an alert by uploading image and storing alert data in Supabase.
    Also sends SMS notifications to rangers via Twilio.
    
    Args:
        image_path (str): Path to the image file
        detection_label (str): Type of detection (e.g., "poacher", "endangered_species")
        location (dict, optional): Dictionary containing lat and lng coordinates
    """
    try:
        print(f"Processing alert for {image_path}...")
        
        # Upload image first
        image_url = upload_image(image_path)
        
        # Copy image to test_images for local viewing
        import shutil
        backend_dir = os.path.dirname(os.path.dirname(__file__))
        test_image_dir = os.path.join(backend_dir, "test_images")
        if not os.path.exists(test_image_dir):
            os.makedirs(test_image_dir)
        original_filename = os.path.basename(image_path)
        test_image_filename = generate_unique_filename(original_filename)
        destination_path = os.path.join(test_image_dir, test_image_filename)
        shutil.copy(image_path, destination_path)
        test_image_url = f"http://localhost:8000/test_images/{test_image_filename}"
        print(f"Test image saved at: {destination_path} with URL: {test_image_url}")
        
        # Get current time in Montreal timezone
        montreal_now = datetime.now(MONTREAL_TZ)
        
        # Prepare alert data
        alert_data = {
            "type": detection_label,
            "image_url": image_url,
            "status": "new",
            "created_at": montreal_now.isoformat()  # Store in ISO format with timezone
        }
        
        if location:
            alert_data["location"] = location
        
        # Insert into Supabase database
        print("Sending alert to database...")
        result = supabase.table("alerts").insert(alert_data).execute()
        
        alert_id = result.data[0]["id"]
        display_time = montreal_now.strftime("%I:%M:%S %p %Z")
        print(f"Alert sent successfully at {display_time}! Alert ID: {alert_id}")
        
        # Send SMS notifications via Twilio
        print("Sending SMS notifications to rangers...")
        notify_all_rangers(detection_label, f"{image_url} | {test_image_url}", location)
        
        return alert_id
        
    except Exception as e:
        print(f"Error sending alert: {e}")
        print("Make sure you've created the 'alerts' table in Supabase using the provided SQL")
        raise

def get_recent_alerts(limit=10):
    """
    Retrieve recent alerts from Supabase.
    
    Args:
        limit (int): Maximum number of alerts to retrieve
        
    Returns:
        list: List of alert dictionaries
    """
    try:
        result = (supabase.table("alerts")
                 .select("*")
                 .order("created_at", desc=True)
                 .limit(limit)
                 .execute())
        
        # Convert timestamps to Montreal time
        alerts = result.data
        for alert in alerts:
            if "created_at" in alert:
                alert["created_at"] = format_datetime_montreal(alert["created_at"])
                
        return alerts
    
    except Exception as e:
        print(f"Error retrieving alerts: {e}")
        raise

def update_alert_status(alert_id, status):
    """
    Update the status of an alert.
    
    Args:
        alert_id (str): ID of the alert
        status (str): New status ('acknowledged' or 'resolved')
    """
    try:
        montreal_now = datetime.now(MONTREAL_TZ)
        
        supabase.table("alerts").update({
            "status": status,
            "updated_at": montreal_now.isoformat()
        }).eq("id", alert_id).execute()
        
        display_time = montreal_now.strftime("%I:%M:%S %p %Z")
        print(f"Alert {alert_id} status updated to: {status} at {display_time}")
        
    except Exception as e:
        print(f"Error updating alert status: {e}")
        raise

# Initialize connection when module is imported
initialize_storage()
