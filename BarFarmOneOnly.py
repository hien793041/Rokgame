import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pyautogui
import time
import random
from bot_utils import click_button, ensure_assets_directory

class Config:
    """Configuration constants for the bot"""
    MAX_RETRIES = 50
    MIN_RETRY_WAIT = 2
    MAX_RETRY_WAIT = 3
    STARTUP_DELAY = 2
    SCREENSHOT_PAUSE = 0.5

# Configure PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = Config.SCREENSHOT_PAUSE

class AssetPaths:
    """Asset file paths for UI elements"""
    BASE_DIR = "assets/barbarian"
    
    FIND_BAR = f"{BASE_DIR}/find_bar_button.png"
    CONFIRM_FIND = f"{BASE_DIR}/confirm_find_button.png"
    ATTACK = f"{BASE_DIR}/attack_button.png"
    ADD_TROOP = f"{BASE_DIR}/add_troop_button.png"
    SELECT_TROOP = f"{BASE_DIR}/select_troop_button.png"
    SEND_TROOP = f"{BASE_DIR}/send_troop_button.png"


def try_click_button(button_path: str, button_name: str) -> bool:
    """Attempt to click a button with retries"""
    for attempt in range(Config.MAX_RETRIES):
        if click_button(button_path):
            time.sleep(random.uniform(1, 3))
            return True
        print(f"Button '{button_name}' not found, retry {attempt + 1}/{Config.MAX_RETRIES}", flush=True)
        time.sleep(random.uniform(Config.MIN_RETRY_WAIT, Config.MAX_RETRY_WAIT))
    
    print(f"Skipping '{button_name}' after {Config.MAX_RETRIES} attempts", flush=True)
    return False

def execute_barbarian_attack_sequence() -> bool:
    """Execute the complete barbarian attack sequence"""
    attack_sequence = [
        (AssetPaths.FIND_BAR, "Find Barbarian"),
        (AssetPaths.CONFIRM_FIND, "Confirm Find"),
        (AssetPaths.ATTACK, "Attack"),
        (AssetPaths.ADD_TROOP, "Add Troops"),
        (AssetPaths.SEND_TROOP, "Send Troops")
    ]
    
    for button_path, button_name in attack_sequence:
        if not try_click_button(button_path, button_name):
            return False
    
    return True

def main():
    """Main bot execution"""
    print(f"RoK Barbarian Farm Bot starting in {Config.STARTUP_DELAY} seconds...")
    time.sleep(Config.STARTUP_DELAY)
    
    try:
        while True:
            print("Starting barbarian attack cycle...", flush=True)
            
            if execute_barbarian_attack_sequence():
                print("Attack cycle completed successfully", flush=True)
            else:
                print("Attack cycle failed, retrying...", flush=True)
            
            time.sleep(random.uniform(Config.MIN_RETRY_WAIT, Config.MAX_RETRY_WAIT))
            
    except KeyboardInterrupt:
        print("Bot stopped by user", flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)

if __name__ == "__main__":
    ensure_assets_directory()
    main()