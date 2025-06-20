import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
import random
from bot_utils import click_button, ensure_assets_directory

class Config:
    """Configuration constants for the fog scout bot"""
    MAX_RETRIES = 200
    MIN_RETRY_WAIT = 1
    MAX_RETRY_WAIT = 2
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.5
    LOAD_WAIT_TIME = 2

# Configure PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = Config.SCREENSHOT_PAUSE

class AssetPaths:
    """Asset file paths for fog scout UI elements"""
    BASE_DIR = "assets/fog"
    
    SCOUT_CAMP = f"{BASE_DIR}/scout_camp.png"
    EXPLORE = f"{BASE_DIR}/explore_button.png"
    CONFIRM = f"{BASE_DIR}/confirm_button.png"
    SEND = f"{BASE_DIR}/send_button.png"
    BACK = f"{BASE_DIR}/back_button.png"


def open_scout_camp() -> bool:
    """Open scout camp interface"""
    print("Opening scout camp...", flush=True)
    
    for attempt in range(Config.MAX_RETRIES):
        if click_button(AssetPaths.SCOUT_CAMP):
            time.sleep(Config.LOAD_WAIT_TIME)
            return True
        print(f"Scout camp not found, retry {attempt + 1}/{Config.MAX_RETRIES}", flush=True)
        time.sleep(random.uniform(3, 5))
    
    print(f"Failed to open scout camp after {Config.MAX_RETRIES} attempts", flush=True)
    return False

def try_click_button_with_retry(button_path: str, button_name: str, wait_time: float = None) -> bool:
    """Attempt to click a button with retries"""
    if wait_time is None:
        wait_time = random.uniform(0.5, 1)
        
    for attempt in range(Config.MAX_RETRIES):
        if click_button(button_path):
            time.sleep(wait_time)
            return True
        print(f"Button '{button_name}' not found, retry {attempt + 1}/{Config.MAX_RETRIES}", flush=True)
        time.sleep(random.uniform(Config.MIN_RETRY_WAIT, Config.MAX_RETRY_WAIT))
    
    print(f"Skipping '{button_name}' after {Config.MAX_RETRIES} attempts", flush=True)
    return False

def send_scout() -> bool:
    """Send scout to explore fog of war"""
    print("Sending scout...", flush=True)
    
    scout_sequence = [
        (AssetPaths.EXPLORE, "Explore", 0.75),
        (AssetPaths.CONFIRM, "First Confirm", 0.75),
        (AssetPaths.CONFIRM, "Second Confirm", 0.75),
        (AssetPaths.SEND, "Send", 0.75),
        (AssetPaths.BACK, "Back", 2.0)
    ]
    
    for button_path, button_name, wait_time in scout_sequence:
        if not try_click_button_with_retry(button_path, button_name, wait_time):
            return False
    
    return True

def execute_fog_scout_cycle() -> bool:
    """Execute complete fog scouting cycle"""
    if not open_scout_camp():
        print("Failed to open scout camp, retrying...", flush=True)
        return False
        
    if not send_scout():
        print("Failed to send scout, retrying...", flush=True)
        return False
        
    return True

def main():
    """Main bot execution"""
    print(f"RoK Fog Scout Bot starting in {Config.STARTUP_DELAY} seconds...", flush=True)
    time.sleep(Config.STARTUP_DELAY)
    
    try:
        while True:
            print("Starting fog scout cycle...", flush=True)
            
            if execute_fog_scout_cycle():
                print("Scout cycle completed successfully", flush=True)
            else:
                print("Scout cycle failed, waiting before retry...", flush=True)
                time.sleep(5)
                continue
                
            time.sleep(random.uniform(Config.MIN_RETRY_WAIT, Config.MAX_RETRY_WAIT))
            
    except KeyboardInterrupt:
        print("Bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)

if __name__ == "__main__":
    ensure_assets_directory()
    main()