import asyncio
from telegram.ext import ApplicationBuilder
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import os

# Telegram Bot Token (you'll get this from @BotFather)
TELEGRAM_BOT_TOKEN = "your_bot_token_here"

# Chat IDs for rangers (you'll get these when rangers start the bot)
RANGER_CHAT_IDS = [
    # Add ranger chat IDs here
]

# Initialize bot application
app = None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Welcome to WildGuard! Your chat ID is: {chat_id}\n"
             f"Share this ID with your administrator to receive alerts."
    )

def initialize_bot():
    """Initialize the Telegram bot"""
    global app
    try:
        # Create bot application
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start_command))
        
        # Start bot in background
        asyncio.create_task(app.initialize())
        asyncio.create_task(app.start())
        
        print("Successfully connected to Telegram")
        return True
    except Exception as e:
        print(f"Error initializing Telegram bot: {e}")
        print("Telegram notifications will be disabled")
        return False

async def send_telegram_alert(detection_type, image_url=None, location=None):
    """
    Send alert to all rangers via Telegram.
    
    Args:
        detection_type (str): Type of detection (e.g., "poacher", "endangered_species")
        image_url (str, optional): URL of the detected image
        location (dict, optional): Dictionary containing lat and lng coordinates
    """
    if not app:
        print("Telegram bot not initialized. Notifications will not be sent.")
        return
    
    try:
        # Format the alert message
        alert_type = detection_type.replace('_', ' ').title()
        message = f"🚨 WildGuard Alert!\n\n"
        message += f"Type: {alert_type}"
        
        if location:
            message += f"\n\n📍 Location:"
            message += f"\nLatitude: {location['lat']}"
            message += f"\nLongitude: {location['lng']}"
            maps_url = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
            message += f"\n\n🗺 View on Maps: {maps_url}"
        
        # Send to all rangers
        for chat_id in RANGER_CHAT_IDS:
            try:
                # Send text message
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='HTML'
                )
                
                # If there's an image, send it
                if image_url:
                    await app.bot.send_photo(
                        chat_id=chat_id,
                        photo=image_url,
                        caption=f"📸 Detected: {alert_type}"
                    )
                
                print(f"Alert sent to ranger (chat_id: {chat_id})")
                
            except Exception as e:
                print(f"Error sending alert to chat_id {chat_id}: {e}")
    
    except Exception as e:
        print(f"Error sending Telegram alerts: {e}")

def notify_rangers(detection_type, image_url=None, location=None):
    """
    Synchronous wrapper for sending Telegram notifications.
    """
    try:
        # Create event loop if it doesn't exist
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Send notifications
    loop.run_until_complete(
        send_telegram_alert(detection_type, image_url, location)
    )

print("To set up the Telegram bot:")
print("1. Message @BotFather on Telegram")
print("2. Create new bot with /newbot command")
print("3. Copy the bot token and update TELEGRAM_BOT_TOKEN")
print("4. Rangers should start the bot and share their chat IDs")
print("5. Add ranger chat IDs to RANGER_CHAT_IDS list")

# Initialize bot when module is imported
if TELEGRAM_BOT_TOKEN != "your_bot_token_here":
    initialize_bot()
else:
    print("Please set TELEGRAM_BOT_TOKEN to enable notifications")