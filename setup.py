import subprocess
import sys
import os
from pathlib import Path

def setup():
    """Setup the WildGuard detection system"""
    print("\n=== Setting up WildGuard Detection System ===\n")

    # Upgrade pip
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Install dependencies
    print("\nInstalling dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Create necessary directories
    print("\nCreating project directories...")
    directories = ['input_images', 'output']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"Created directory: {dir_name}/")

    print("\nSetup complete! You can now run: python test_detection.py")

if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)